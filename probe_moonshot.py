import os
import json
import time
from groq import Groq

# --- CONFIG ---
MODEL = "moonshotai/kimi-k2-instruct-0905"
LOG_FILE = "moonshot_probe_results.log"

def get_api_key():
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GROQ_KEYS="):
                    # Format: key1,key2 or label:key1,label:key2
                    raw = line.strip().split("=", 1)[1]
                    first_entry = raw.split(",")[0]
                    if ":" in first_entry:
                        return first_entry.split(":")[1]
                    return first_entry
    except Exception as e:
        print(f"Error reading .env: {e}")
        return None

KEY = get_api_key()
if not KEY:
    print("FATAL: Could not find GROQ_KEYS in .env")
    exit(1)

client = Groq(api_key=KEY)

def log(header, content):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n{'='*60}\n[{timestamp}] {header}\n{'='*60}\n{content}\n"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry)

def run_test(name, messages, **kwargs):
    print(f"Running Test: {name}...")
    try:
        start = time.time()
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            **kwargs
        )
        duration = time.time() - start
        
        content = completion.choices[0].message.content
        log(f"TEST: {name} (Duration: {duration:.2f}s)", f"PARAMS: {kwargs}\n\nOUTPUT:\n{content}")
        return content
    except Exception as e:
        log(f"TEST FAILED: {name}", f"ERROR: {str(e)}")
        return None

# --- SCENARIOS ---

# 1. BASELINE
run_test("BASELINE_TEXT", 
    [{"role": "user", "content": "Return a JSON object with fields 'name' and 'age' for a fictional character."}],
    temperature=0.7
)

# 2. JSON MODE (Explicit)
run_test("JSON_MODE_OBJECT",
    [
        {"role": "system", "content": "You are a helpful assistant. Output JSON."},
        {"role": "user", "content": "Return a JSON object with fields 'name' and 'age' for a fictional character."}
    ],
    response_format={"type": "json_object"},
    temperature=0.7
)

# 3. SCHEMA (Theoretical)
# Trying to pass a schema if supported, or mocking it via prompt + json mode
run_test("JSON_SCHEMA_SIMULATION",
    [
         {"role": "system", "content": "You are a helpful assistant. Output valid JSON matching the schema: {name: str, age: int, skills: []}."},
         {"role": "user", "content": "Generate a character profile."}
    ],
    response_format={"type": "json_object"},
    temperature=0.5
)

# 4. EAGLE PROMPT SIMULATION (The Real Deal)
# This mimics the actual prompt usage to see the raw output format (Project Tree vs Code Blocks)
EAGLE_PROMPT = """
ACT AS EAGLE, A SENIOR REACT ARCHITECT.
Transform the following architecture into a SCAFFOLDING structure.
OUTPUT RULES:
1. Do not use Markdown code blocks for the specific files yet, just list the file tree.
2. Actually, wait, the user wants the CODE.
   Okay, output the file tree first, then the files using this format:

### filename.ext
```javascript
code here
```

PROJECT: User Dashboard
FILES:
- src/components/Dashboard.tsx
- src/utils/api.ts

GO.
"""

run_test("EAGLE_SIMULATION",
    [{"role": "user", "content": EAGLE_PROMPT}],
    temperature=0.3
)
