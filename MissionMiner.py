#!/usr/bin/env python3

import os
import re
import json
import shutil
import logging
from pathlib import Path
from collections import defaultdict

# ====================== CONFIG ======================
BASE_DIR = Path("/home/flintx/chat_logs")
WASHED_DIR = BASE_DIR / "washed"
STRIKE_READY_DIR = Path("/home/flintx/STRIKE_READY")
MISSION_VAULT_DIR = Path("/home/flintx/MissionVault")
LOG_FILE = Path("/home/flintx/ai-handler/mission_miner.log")

# Setup directories
STRIKE_READY_DIR.mkdir(parents=True, exist_ok=True)
MISSION_VAULT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

def normalize_name(filename):
    """
    Strips 'branch_of_', 'copy_of_', YYYYMMDD prefixes, and extensions to find the root identity.
    """
    name = filename.lower()
    # Strip common prefixes
    name = re.sub(r'^(branch_of_|copy_of_|copy\.of\.)+', '', name)
    # Strip date prefixes (8 digits followed by a dot)
    name = re.sub(r'^\d{8}\.', '', name)
    # Strip extensions
    name = Path(name).stem
    return name.strip()

# ====================== PROMPT ======================
EXTRACTION_PROMPT = """
Analyze this log and extract universal intelligence.
Output ONLY valid JSON.

JSON Structure:
{{
  "overview": "1-2 sentence summary.",
  "categorization": {{
    "app_building": {{ "app_name": "", "features": [], "tech_stack": [], "buildability_score": 1-10 }},
    "app_ideas": {{ "details": "", "takeaways": [] }},
    "philosophy": {{ "details": "", "takeaways": [] }},
    "personal": {{ "details": "", "takeaways": [] }},
    "technical_troubleshooting": {{ "details": "", "takeaways": [] }},
    "miscellaneous": {{ "details": "", "takeaways": [] }}
  }},
  "chroma_front_matter": {{
    "semantic_summary": "200 word essence for vector search.",
    "key_phrases": ["10-20 search phrases"]
  }}
}}

Analyze this chat:
{chat_content}
"""

def scan_and_deduplicate():
    """
    Scans ~/chat_logs recursively and picks the largest file for each root name.
    """
    intel_pool = defaultdict(list)
    extensions = {'.md', '.json', '.txt'}
    
    logging.info(f"Searching for logs in {BASE_DIR}...")
    
    for root, dirs, files in os.walk(BASE_DIR):
        if any(x in root for x in [str(STRIKE_READY_DIR), str(MISSION_VAULT_DIR)]):
            continue
            
        for file in files:
            path = Path(root) / file
            if path.suffix.lower() in extensions:
                root_name = normalize_name(file)
                size = path.stat().st_size
                intel_pool[root_name].append({
                    'path': path,
                    'size': size,
                    'name': file
                })

    final_selection = {}
    for root_name, versions in intel_pool.items():
        winner = max(versions, key=lambda x: x['size'])
        final_selection[root_name] = winner
        
    return final_selection

def prepare_strike_ready(selection):
    """
    Copies selected master logs to STRIKE_READY.
    """
    # Clear existing to avoid stale dupes if re-running triage
    if STRIKE_READY_DIR.exists():
        shutil.rmtree(STRIKE_READY_DIR)
    STRIKE_READY_DIR.mkdir(parents=True, exist_ok=True)

    app_indicators = ['code', 'app', 'react', 'python', 'docker', 'api', 'fix', 'error', 'architecture', 'nexus', 'peacock']
    
    count = 0
    for root_name, info in selection.items():
        if any(word in root_name for word in app_indicators):
            dest = STRIKE_READY_DIR / info['name']
            shutil.copy2(info['path'], dest)
            count += 1
                
    logging.info(f"Staged {count} logs to {STRIKE_READY_DIR}.")

import requests
import time

ENGINE_URL = "http://localhost:3099/v1/strike"
MODELS_URL = "http://localhost:3099/v1/models"

def strike_engine(prompt, model_id="models/gemini-2.0-flash-exp"):
    payload = {"modelId": model_id, "prompt": prompt, "temp": 0.3}
    try:
        resp = requests.post(ENGINE_URL, json=payload, timeout=60)
        if resp.status_code == 200:
            return resp.json().get("content", "")
    except Exception as e:
        logging.error(f"API Error: {e}")
    return None

def clean_json(text):
    if not text: return None
    text = text.strip()
    if text.startswith("```json"): text = text[7:]
    elif text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    try:
        return json.loads(text.strip())
    except:
        return None

def mass_strike_intel(sample_size=10):
    """
    Runs the extraction strike on a sample of logs in STRIKE_READY.
    """
    files = [f for f in STRIKE_READY_DIR.glob("*") if f.is_file() and f.suffix in ['.md', '.txt']]
    sample = files[:sample_size]
    
    logging.info(f"Starting limited strike on {len(sample)} logs...")
    
    manifest = []
    
    for path in sample:
        try:
            with open(path, 'r') as f:
                content = f.read()[:15000] # Cap for flash
            
            prompt = EXTRACTION_PROMPT.format(chat_content=content)
            logging.info(f"Striking: {path.name}")
            
            raw_response = strike_engine(prompt)
            data = clean_json(raw_response)
            
            if data:
                # Save individual analysis
                vault_path = MISSION_VAULT_DIR / f"{path.stem}.intel.json"
                with open(vault_path, 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Add to manifest
                manifest.append({
                    "file": path.name,
                    "overview": data.get("overview", "No summary."),
                    "keywords": data.get("chroma_front_matter", {}).get("key_phrases", []),
                    "buildability": data.get("categorization", {}).get("app_building", {}).get("buildability_score", 0)
                })
        except Exception as e:
            logging.error(f"Failed analysis for {path.name}: {e}")

    # Generate Master Manifest
    if manifest:
        manifest_path = BASE_DIR / "MasterManifest.md"
        with open(manifest_path, 'w') as f:
            f.write("# 🧠 UNIVERSAL MEMORY: MASTER MANIFEST\n\n")
            for item in manifest:
                f.write(f"## {item['file']}\n")
                f.write(f"- **Summary**: {item['overview']}\n")
                f.write(f"- **Keywords**: {', '.join(item['keywords'])}\n")
                f.write(f"- **Buildability**: {item['buildability']}/10\n\n")
        
        logging.info(f"Master Manifest generated at {manifest_path}")

def main():
    selection = scan_and_deduplicate()
    prepare_strike_ready(selection)
    mass_strike_intel(sample_size=10)
    logging.info("Test Strike Complete.")
    print(f"\n[⚡ TEST STRIKE COMPLETE]")
    print(f"Manifest ready at: {BASE_DIR / 'MasterManifest.md'}")

if __name__ == "__main__":
    main()
