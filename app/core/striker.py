import os
import httpx
from typing import List, Optional
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.google import GoogleProvider
from app.core.key_manager import GroqPool, GooglePool, DeepSeekPool, MistralPool

# Proxy Setup
proxy_url = os.getenv("PROXY_URL")
proxy_enabled = os.getenv("PROXY_ENABLED") == "true"
http_client = httpx.AsyncClient(proxy=proxy_url) if proxy_enabled and proxy_url else httpx.AsyncClient()

# --- STRUCTURED OUTPUT MODELS ---
class EagleFile(BaseModel):
    path: str
    skeleton: str
    directives: str

class EagleScaffold(BaseModel):
    project: str
    files: List[EagleFile]

# --------------------------------

async def execute_strike(gateway: str, model_id: str, prompt: str, temp: float, format_mode: Optional[str] = None):
    # Determine Result Type
    result_type = str
    if format_mode == "eagle_scaffold":
        result_type = EagleScaffold

    model = None
    asset = None

    if gateway == "groq":
        asset = GroqPool.get_next()
        print(f"[💥 STRIKE] ACC: {asset.account.ljust(15)} | GW: GROQ | FMT: {format_mode}")
        provider = GroqProvider(api_key=asset.key, http_client=http_client)
        model = GroqModel(model_id, provider=provider)

    elif gateway == "deepseek":
        asset = DeepSeekPool.get_next()
        print(f"[💥 STRIKE] ACC: {asset.account.ljust(15)} | GW: DEEPSEEK | FMT: {format_mode}")
        provider = OpenAIProvider(
            base_url="https://api.deepseek.com", 
            api_key=asset.key,
            http_client=http_client
        )
        model = OpenAIModel(model_id, provider=provider)

    elif gateway == "mistral":
        asset = MistralPool.get_next()
        print(f"[💥 STRIKE] ACC: {asset.account.ljust(15)} | GW: MISTRAL | FMT: {format_mode}")
        provider = OpenAIProvider(
            base_url="https://api.mistral.ai/v1",
            api_key=asset.key,
            http_client=http_client
        )
        model = OpenAIModel(model_id, provider=provider)

    elif gateway == "google":
        asset = GooglePool.get_next()
        print(f"[💥 STRIKE] ACC: {asset.account.ljust(15)} | GW: GOOGLE | FMT: {format_mode}")
        clean_model_id = model_id.replace("models/", "")
        provider = GoogleProvider(api_key=asset.key, http_client=http_client)
        model = GoogleModel(clean_model_id, provider=provider)

    else:
        raise Exception(f"Gateway {gateway} not supported")

    # SPECIAL HANDLING FOR MOONSHOT/KIMI (Force JSON Mode)
    if format_mode == "eagle_scaffold" and ("moonshot" in model_id or "kimi" in model_id) and gateway == "groq":
        from groq import AsyncGroq
        import json
        
        print(f"[💥 STRIKE] ACC: {asset.account.ljust(15)} | GW: GROQ | FMT: eagle_scaffold (JSON MODE BYPASS)")
        
        # 1. Prepare Schema
        schema = json.dumps(EagleScaffold.model_json_schema(), indent=2)
        
        # 2. Prepare Messages
        messages = [
            {
                "role": "system", 
                "content": f"You are a Senior React Architect. Output valid JSON matching the following schema:\n{schema}\n\nIMPORTANT: Return ONLY the JSON object. No markdown, no explanations."
            },
            {"role": "user", "content": prompt}
        ]
        
        try:
            # 3. Direct Client Init
            client = AsyncGroq(api_key=asset.key, http_client=http_client)
            
            completion = await client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=temp,
                response_format={"type": "json_object"}
            )
            
            raw_json = completion.choices[0].message.content
            print(f"[🛡️ MOONSHOT] JSON Received ({len(raw_json)} chars)")
            
            # 4. Parse & Validate
            data = json.loads(raw_json)
            validated = EagleScaffold(**data)
            return validated.model_dump()
            
        except Exception as e:
            print(f"[⚠️ MOONSHOT FAILURE] {e}")
            # Fallthrough to standard logic or re-raise
            # If JSON parse fails, we might want to let the standard Agent try, or just fail.
            # But let's assume if this fails, we are cooked anyway.
            raise e

    # Execute Agent (Standard Path)
    agent = Agent(model, output_type=result_type)
    try:
        result = await agent.run(prompt)
        # Return raw data (Pydantic model turned to dict if structured)
        content = result.output.model_dump() if format_mode else result.output
        
    except Exception as e:
        # RESCUE STRATEGY for models that refuse to use tools (like Moonshot)
        # They often throw 400 tool_use_failed but return the content in 'failed_generation'
        
        error_body = getattr(e, "body", {})
        if not error_body:
             # Try to dig deeper if it's wrapped
            if hasattr(e, "__cause__") and hasattr(e.__cause__, "body"):
                 error_body = e.__cause__.body

        failed_gen = error_body.get("error", {}).get("failed_generation") if error_body else None
        
        if failed_gen and format_mode == "eagle_scaffold":
            print(f"[🛡️ RESCUE] Parsing failed_generation content explicitly...")
            import re
            files = []
            
            # STRATEGY 1: JSON Block
            try:
                import json
                json_start = failed_gen.find('{')
                json_end = failed_gen.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    data = json.loads(failed_gen[json_start:json_end])
                    if 'files' in data:
                        for f in data['files']:
                            files.append(EagleFile(path=f['path'], skeleton=f.get('skeleton', ''), directives=f.get('directives', '')))
                        print(f"[✅ RESCUE JSON] Recovered {len(files)} files.")
            except:
                pass

            if not files:
                # STRATEGY 2: Markdown Code Blocks (filename header)
                # Matches: **filename: path** ... ```code```
                print(f"[DEBUG RAW] {failed_gen[:500]}...") # Print first 500 chars to debug
                pattern_md = r"\*\*filename:\s*(.*?)\*\*\s*```[\w]*\n(.*?)```"
                matches_md = re.findall(pattern_md, failed_gen, re.DOTALL)
                for path, code in matches_md:
                    files.append(EagleFile(path=path.strip(), skeleton=code.strip(), directives="Parsed from Markdown"))

            if not files:
                # STRATEGY 3: EOF Blocks (cat << 'EOF' > path)
                pattern_eof = r"cat << 'EOF' >\s*(\S+)\s*\n(.*?)EOF"
                matches_eof = re.findall(pattern_eof, failed_gen, re.DOTALL)
                for path, code in matches_eof:
                    files.append(EagleFile(path=path.strip(), skeleton=code.strip(), directives="Parsed from EOF Block"))
            
            if not files:
                # STRATEGY 4: Aggressive Header Match
                # Matches: ### path/to/file ... ```code```
                # OR Matches: File: path/to/file ... ```code```
                pattern_aggressive = r"(?:###|File:)\s*(\S+).*?```[\w]*\n(.*?)```"
                matches_agg = re.findall(pattern_aggressive, failed_gen, re.DOTALL)
                for path, code in matches_agg:
                    files.append(EagleFile(path=path.strip(), skeleton=code.strip(), directives="Parsed from Aggressive Search"))

            if not files:
                # STRATEGY 5: PROJECT_TREE (The "Reality" Parser)
                # Parse the visual tree structure to extract valid file paths.
                # 1. Extract Directives
                directives = "Follow standard implementation patterns."
                dir_match = re.search(r"### DIRECTIVES(.*?)(?:###|$)", failed_gen, re.DOTALL)
                if dir_match:
                    directives = dir_match.group(1).strip()
                
                # 2. Extract Files using Stack-Based Indentation Tracking
                # We track the current directory path based on indentation/depth.
                
                # Regex to identify lines. Captures:
                # 1. Indentation/Prefix (│  ├─ etc)
                # 2. Name (dirname or filename)
                # Note: We look for the LAST component of the tree prefix to judge depth.
                
                lines = failed_gen.split('\n')
                path_stack = [] # Stores current directory components
                
                for line in lines:
                    if not line.strip(): continue
                    
                    # Pattern matches tree markers like ├─, └─, │
                    # We calculate depth by counting constant-width characters or finding the marker index.
                    # Standard tree output usually steps by 3 or 4 chars.
                    
                    # Check if line looks like a tree node
                    tree_match = re.search(r"^([│\s]*(?:├──|└──))\s*(.+)$", line)
                    if not tree_match:
                        # Root folders often look like "folder/" without tree markers in some outputs
                        # But for now, let's stick to the tree structure.
                        # If a line is just "src/", it might be root.
                        basic_match = re.search(r"^(\w+)/$", line)
                        if basic_match:
                            path_stack = [basic_match.group(1)]
                        continue

                    prefix = tree_match.group(1)
                    name = tree_match.group(2).strip()
                    
                    # Calculate depth based on the length of the prefix or count of '│' and indentation
                    # Typically: 
                    # ├── is depth 0 relative to parent? No.
                    # Standard Kimi output:
                    # caseflow-pro/      (Root, usually handled prior)
                    # ├─ public/         (Depth 1)
                    # │  ├─ index.html   (Depth 2)
                    
                    # We can estimate depth by strictly counting spaces/bars before the ├ └
                    # Each level is approx 3-4 chars "│  "
                    
                    # Heuristic: Count valid "depth units" (│  )
                    depth_units = prefix.count("│  ") + prefix.count("   ")
                    
                    # The stack should match the depth.
                    # If depth 0, we are at root (or under the explicit root).
                    # If we are deeper, we append.
                    # If we are shallower, we pop.
                    
                    # Kimi's specific format from log:
                    # ├─ public/
                    # │  ├─ data/
                    # │  │  └─ search_index.json
                    
                    # The depth is fairly clean:
                    # ├─ (Level 0)
                    # │  ├─ (Level 1)
                    # │  │  └─ (Level 2)
                    
                    current_depth = prefix.count("│") + prefix.count("  ") // 2 # Rough heuristic
                    
                    # Better Approach:
                    # Just manage the stack.
                    # If it ends with /, it's a dir -> Add to stack (after adjusting depth)
                    # If it has an extension, it's a file -> Emit path
                    
                    # Let's rely on the visual depth of the marker "├──" or "└──"
                    marker_index = line.find("├") 
                    if marker_index == -1: marker_index = line.find("└")
                    if marker_index == -1: continue 
                    
                    # This raw index is a great proxy for depth.
                    # root items usually at index 0 or 2.
                    # items inside them at index 4, 5, or 6.
                    
                    # We can map indentation index to stack levels.
                    # This is brittle but effective for fixed-width response.
                    
                    # Let's try a pure path logic:
                    # If name ends with /, it's a dir.
                    # If name has extension, it's a file.
                    # But we need the parent.
                    
                    # Let's use the Python logic provided in similar libraries:
                    # Count nesting level (spaces / 4 or similar)
                    
                    level = marker_index // 3 # Every 3-4 chars is a level
                    
                    # Adjust stack
                    # If we are at level L, we want stack to have L items.
                    if level < len(path_stack):
                        path_stack = path_stack[:level]
                    elif level > len(path_stack):
                        # This shouldn't happen in valid tree unless we missed a step
                        # But we can just append a placeholder if needed, or ignore
                        pass
                        
                    if name.endswith("/") or "." not in name: # Directory
                        # Clean name
                        clean_name = name.rstrip("/")
                        if len(path_stack) == level:
                            path_stack.append(clean_name)
                        else:
                            # Re-align
                            path_stack = path_stack[:level]
                            path_stack.append(clean_name)
                    else:
                        # It is a file
                        full_path = "/".join(path_stack + [name])
                        # Filter junk
                        if name not in ["README.md", "styles.css", "index.html", ".DS_Store"]:
                            files.append(EagleFile(path=full_path, skeleton=f"// SKELETON FOR {full_path}", directives=directives))

                # Fallback if tree parsing yields nothing but we saw code blocks
                if not files and matches_agg:
                     for path, code in matches_agg:
                        files.append(EagleFile(path=path.strip(), skeleton=code.strip(), directives="Parsed from Aggressive Search"))

            rescued_scaffold = EagleScaffold(project="Rescued Project for User", files=files)
            content = rescued_scaffold.model_dump()
            print(f"[✅ RESCUE FINAL] Recovered {len(files)} files.")
        else:
            print(f"[❌ STRIKE ERROR] {str(e)}")
            raise e
    
    return {"content": content, "keyUsed": asset.account}
