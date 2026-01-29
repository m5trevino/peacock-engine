import os
import json
import time
import httpx
from groq import Groq

# --- CONFIGURATION ---
MODEL = "moonshotai/kimi-k2-instruct-0905"
ENV_PATH = "/home/flintx/ai-handler/.env"
RESULTS_FILE = "owl_probe_results.json"

# --- INFRASTRUCTURE ---
def load_config():
    config = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    config[key] = val
    return config

config = load_config()
GROQ_KEYS = config.get("GROQ_KEYS", "").split(",")
# Use the first key for testing
FIRST_KEY = GROQ_KEYS[0].split(":")[1] if ":" in GROQ_KEYS[0] else GROQ_KEYS[0]

PROXY_URL = config.get("PROXY_URL")
PROXY_ENABLED = config.get("PROXY_ENABLED") == "true"

http_client = httpx.Client(proxy=PROXY_URL) if PROXY_ENABLED and PROXY_URL else httpx.Client()
client = Groq(api_key=FIRST_KEY, http_client=http_client)

def run_probe(name, messages, response_format=None, temp=0.7):
    print(f"\n[🚀 PROBE] :: {name}...")
    try:
        start = time.time()
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format=response_format,
            temperature=temp
        )
        duration = time.time() - start
        
        raw_content = completion.choices[0].message.content
        print(f"[✅ SUCCESS] :: {duration:.2f}s")
        
        # Test Parsability
        parsed = None
        error = None
        try:
            parsed = json.loads(raw_content)
        except Exception as e:
            error = str(e)
            
        return {
            "test_name": name,
            "duration": duration,
            "raw_output": raw_content,
            "parsable": parsed is not None,
            "parse_error": error,
            "parsed_data": parsed
        }
    except Exception as e:
        print(f"[❌ FAILED] :: {str(e)}")
        return {"test_name": name, "error": str(e)}

# --- TEST SUITE ---
SYSTEM_PROMPT = "ACT AS OWL. FLESH OUT THE SKELETON PER THE DIRECTIVES. OUTPUT JSON ONLY."
USER_INPUT = """
FILE_PATH: src/utils/math.ts
DIRECTIVES: Implement a complex prime number generator using the Sieve of Eratosthenes.
SKELETON_CODE:
export const getPrimes = (limit: number): number[] => {
    // TODO: Implement logic
    return [];
}
"""

tests = []

# Test 1: JSON_OBJECT Mode (App Default)
tests.append(run_probe(
    "JSON_OBJECT_MODE",
    [
        {"role": "system", "content": f"{SYSTEM_PROMPT} SCHEMA: {{ \"path\": \"str\", \"code\": \"str\" }}"},
        {"role": "user", "content": USER_INPUT}
    ],
    response_format={"type": "json_object"}
))

# Test 2: JSON_SCHEMA Mode (Strict: False)
tests.append(run_probe(
    "JSON_SCHEMA_MODE_SOFT",
    [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_INPUT}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "owl_flesh_out",
            "schema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "code": {"type": "string"}
                },
                "required": ["path", "code"],
                "additionalProperties": False
            }
        }
    }
))

# Test 3: Raw Text with Explicit XML-like Envelopes (Fallback)
tests.append(run_probe(
    "RAW_TEXT_ENVELOPE",
    [
        {"role": "system", "content": "ACT AS OWL. WRAP YOUR CODE IN <OWL_CODE> TAGS. DO NOT OUTPUT ANYTHING ELSE."},
        {"role": "user", "content": USER_INPUT}
    ],
    temp=0.3
))

# --- OUTPUT ---
with open(RESULTS_FILE, "w") as f:
    json.dump(tests, f, indent=2)

print(f"\n[📊 RESULTS] :: Saved to {RESULTS_FILE}")
