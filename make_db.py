#!/home/flintx/ai-chats/.venv/bin/python3
"""
PEACOCK MEMORY: Standalone Database Creator
Creates ChromaDB from 1,385 chat files in ~/ai-chats/
"""

import os
import re
import json
import hashlib
import asyncio
import aiohttp
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import chromadb
from chromadb.config import Settings
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn

# CONFIGURATION
CHAT_DIRS = [
    "/home/flintx/ai-chats/aistudio",
    "/home/flintx/ai-chats/chatgpt", 
    "/home/flintx/ai-chats/claude"
]
CHROMA_PATH = "/home/flintx/ai-chats/chroma-db/peacock-memory"
PEACOCK_URL = "http://localhost:3099"
CHECKPOINT_FILE = f"{CHROMA_PATH}/checkpoint.json"
BATCH_SIZE = 50

console = Console()

@dataclass
class Exchange:
    user: str
    ai: str
    entry_num: str
    platform: str
    file: str
    timestamp: Optional[str] = None

class PeacockClient:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.available = False
        
    async def connect(self):
        self.session = aiohttp.ClientSession()
        try:
            async with self.session.get(f"{PEACOCK_URL}/health", timeout=5):
                self.available = True
                console.print("[green]✓ Peacock Engine connected[/green]")
        except:
            console.print("[yellow]⚠ Peacock unavailable — using fallback rules[/yellow]")
    
    async def close(self):
        if self.session:
            await self.session.close()
    
    async def classify(self, text: str) -> Dict:
        """Classify exchange into vault + extract metadata"""
        if not self.available:
            return self._rule_based(text)
        
        prompt = f"""Classify this chat exchange into exactly one vault:
- tech_vault: Code, Peacock, Social Lube, APIs, Linux, scripts
- case_files_vault: True crime, legal, investigations  
- personal_vault: Spiritual, family, goals, personal
- seed_vault: Unassigned ideas, embryonic concepts

Extract: project name (if tech), maturity (embryonic/exploring/committed/abandoned/completed), has_code (bool), topics (list)

Return JSON: {{"vault": "...", "project": "...", "maturity": "...", "has_code": bool, "topics": []}}

TEXT:
{text[:2000]}"""
        
        try:
            async with self.session.post(
                f"{PEACOCK_URL}/v1/strike",
                json={"modelId": "llama3-8b-8192", "prompt": prompt, "temp": 0.1},
                timeout=30
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return json.loads(data.get("content", "{}"))
        except:
            pass
        
        return self._rule_based(text)
    
    def _rule_based(self, text: str) -> Dict:
        """Fallback classification without Peacock"""
        t = text.lower()
        tech = ["peacock", "social-lube", "code", "api", "python", "react", "chroma", "function", "class", "def "]
        case = ["kohberger", "crime", "court", "legal", "transcript", "investigation"]
        personal = ["spiritual", "family", "goal", "personal", "wife", "girlfriend", "meditation"]
        
        if any(s in t for s in case):
            return {"vault": "case_files_vault", "project": None, "maturity": "uncertain", "has_code": False, "topics": []}
        elif any(s in t for s in personal):
            return {"vault": "personal_vault", "project": None, "maturity": "uncertain", "has_code": False, "topics": []}
        elif any(s in t for s in tech):
            project = "peacock" if "peacock" in t else "social-lube" if "social" in t else None
            return {"vault": "tech_vault", "project": project, "maturity": "uncertain", "has_code": "```" in t, "topics": []}
        return {"vault": "seed_vault", "project": None, "maturity": "embryonic", "has_code": False, "topics": []}
    
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings via Peacock (uses 3 Google keys)"""
        if not self.available:
            raise Exception("Peacock down — cannot embed")
        
        async with self.session.post(
            f"{PEACOCK_URL}/v1/strike",
            json={"modelId": "gemini-embedding-exp-03-07", "input": texts, "task_type": "RETRIEVAL_DOCUMENT"},
            timeout=60
        ) as resp:
            if resp.status == 200:
                return (await resp.json()).get("embeddings", [])
            raise Exception(f"Embedding failed: {resp.status}")

class Parser:
    """Parse ASCII-bordered chat logs"""
    
    PATTERN = re.compile(
        r'[┎━─━┒┍──━┑╔═══╗].*?\[(USER ENTRY|GEMINI RESPONSE|CLAUDE RESPONSE|CHATGPT RESPONSE)\s*#(\d+)\].*?[┖━─━┚┕──━┙╚═══╝](.*?)(?=[┎━─━┒┍──━┑╔═══╗]|$)',
        re.DOTALL | re.IGNORECASE
    )
    
    PLATFORM = {"USER ENTRY": "USER", "GEMINI RESPONSE": "GEMINI", 
                "CLAUDE RESPONSE": "CLAUDE", "CHATGPT RESPONSE": "CHATGPT"}
    
    def parse(self, path: Path) -> List[Exchange]:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return []
        
        if len(content) < 50:
            return []
        
        matches = list(self.PATTERN.finditer(content))
        exchanges = []
        i = 0
        
        while i < len(matches) - 1:
            curr, nxt = matches[i], matches[i+1]
            curr_type = curr.group(1).upper()
            nxt_type = nxt.group(1).upper()
            
            if "USER" in curr_type and "USER" not in nxt_type:
                exchanges.append(Exchange(
                    user=curr.group(3).strip(),
                    ai=nxt.group(3).strip(),
                    entry_num=curr.group(2),
                    platform=self.PLATFORM.get(nxt_type, "UNKNOWN"),
                    file=str(path),
                    timestamp=self._extract_date(path.name)
                ))
                i += 2
            else:
                i += 1
        
        return exchanges
    
    def _extract_date(self, name: str) -> Optional[str]:
        if m := re.search(r'(\d{2})\.(\d{2})\.(\d{2})', name):
            mm, dd, yy = m.groups()
            return f"20{yy}-{mm}-{dd}"
        return None

class Database:
    """ChromaDB + SQLite manager"""
    
    VAULTS = ["tech_vault", "case_files_vault", "personal_vault", "seed_vault"]
    
    def __init__(self):
        os.makedirs(CHROMA_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings(anonymized_telemetry=False))
        self.collections = {v: self.client.get_or_create_collection(v, metadata={"hnsw:space": "cosine"}) 
                          for v in self.VAULTS}
        self._init_sqlite()
    
    def _init_sqlite(self):
        db = sqlite3.connect(f"{CHROMA_PATH}/index.db")
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY, content TEXT, vault TEXT, project TEXT,
            platform TEXT, timestamp TEXT, maturity TEXT, file TEXT, has_code INTEGER
        )""")
        c.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(
            content, vault, project, maturity, content='chunks', content_rowid='rowid'
        )""")
        db.commit()
        db.close()
    
    def store(self, chunk_id: str, content: str, vault: str, meta: Dict, embedding: List[float]):
        # Chroma
        self.collections[vault].upsert(
            ids=[chunk_id],
            documents=[content],
            embeddings=[embedding],
            metadatas=[{
                "file": meta["file"], "entry": meta["entry"], "platform": meta["platform"],
                "project": meta.get("project", "unknown"), "maturity": meta["maturity"],
                "has_code": meta["has_code"], "topics": ",".join(meta.get("topics", []))
            }]
        )
        
        # SQLite
        db = sqlite3.connect(f"{CHROMA_PATH}/index.db")
        c = db.cursor()
        c.execute("INSERT OR REPLACE INTO chunks VALUES (?,?,?,?,?,?,?,?,?)",
            (chunk_id, content, vault, meta.get("project"), meta["platform"], 
             meta.get("timestamp"), meta["maturity"], meta["file"], int(meta["has_code"])))
        db.commit()
        db.close()

class Checkpoint:
    """Resume capability"""
    
    def __init__(self):
        self.data = {"processed": {}, "total": 0}
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE) as f:
                self.data = json.load(f)
    
    def is_done(self, path: Path) -> bool:
        h = hashlib.md5(path.read_bytes()).hexdigest()
        return h in self.data["processed"]
    
    def mark(self, path: Path, chunks: int, vault: str):
        h = hashlib.md5(path.read_bytes()).hexdigest()
        self.data["processed"][h] = {"file": str(path), "chunks": chunks, "vault": vault, 
                                     "time": datetime.now().isoformat()}
        self.data["total"] += chunks
        with open(CHECKPOINT_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def stats(self):
        return self.data

async def main():
    peacock = PeacockClient()
    await peacock.connect()
    
    parser = Parser()
    db = Database()
    checkpoint = Checkpoint()
    
    # Collect files
    files = []
    for d in CHAT_DIRS:
        if Path(d).exists():
            files.extend(Path(d).rglob("*.md"))
    
    files = [f for f in files if not checkpoint.is_done(f)]
    
    if not files:
        console.print("[green]All files already processed![/green]")
        return
    
    console.print(f"[bold cyan]Processing {len(files)} files...[/bold cyan]")
    
    with Progress(TextColumn("[progress.description]{task.description}"), 
                  BarColumn(), TextColumn("{task.percentage:>3.0f}%"), 
                  TimeElapsedColumn(), console=console) as progress:
        
        task = progress.add_task("[cyan]Ingesting...", total=len(files))
        sem = asyncio.Semaphore(3)  # Rate limit
        
        async def process(f: Path):
            async with sem:
                exchanges = parser.parse(f)
                if not exchanges:
                    progress.advance(task)
                    return 0
                
                # Classify and batch embed
                batch = []
                for ex in exchanges:
                    full = f"USER: {ex.user}\n\n{ex.platform}: {ex.ai}"
                    cls = await peacock.classify(full)
                    batch.append({
                        "id": f"{f.name}_{ex.entry_num}_{ex.platform}",
                        "content": full, "exchange": ex, "class": cls
                    })
                
                # Embed batch
                texts = [b["content"] for b in batch]
                try:
                    embeddings = await peacock.embed(texts)
                    
                    for b, emb in zip(batch, embeddings):
                        db.store(
                            b["id"], b["content"], b["class"]["vault"],
                            {
                                "file": b["exchange"].file, "entry": b["exchange"].entry_num,
                                "platform": b["exchange"].platform, "timestamp": b["exchange"].timestamp,
                                "project": b["class"].get("project"), "maturity": b["class"]["maturity"],
                                "has_code": b["class"]["has_code"], "topics": b["class"].get("topics", [])
                            },
                            emb
                        )
                    
                    primary = max(set(b["class"]["vault"] for b in batch), key=lambda v: sum(1 for b in batch if b["class"]["vault"]==v))
                    checkpoint.mark(f, len(batch), primary)
                    
                except Exception as e:
                    console.print(f"[red]Failed {f.name}: {e}[/red]")
                
                progress.advance(task)
                return len(batch)
        
        results = await asyncio.gather(*[process(f) for f in files])
    
    total = sum(results)
    stats = checkpoint.stats()
    
    console.print(f"\n[bold green]✓ Created database with {total} chunks[/bold green]")
    console.print(f"[dim]Location: {CHROMA_PATH}[/dim]")
    console.print(f"[dim]Checkpoint: {CHECKPOINT_FILE}[/dim]")
    
    # Show vault distribution
    vault_counts = {}
    for v in db.VAULTS:
        vault_counts[v] = db.collections[v].count()
    
    for v, c in vault_counts.items():
        console.print(f"  {v}: {c} chunks")

if __name__ == "__main__":
    asyncio.run(main())