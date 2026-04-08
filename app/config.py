from pydantic import BaseModel
from typing import List, Literal, Optional
import json
from pathlib import Path

class ModelConfig(BaseModel):
    id: str
    gateway: Literal['groq', 'google', 'deepseek', 'mistral']
    tier: Literal['free', 'cheap', 'expensive', 'custom', 'deprecated']
    note: str
    status: Literal['active', 'frozen', 'deprecated'] = 'active'
    context_window: Optional[int] = None
    # Rate Limits
    rpm: Optional[int] = None
    tpm: Optional[int] = None
    rpd: Optional[int] = None
    # Pricing (per 1M tokens)
    input_price_1m: float = 0.0
    output_price_1m: float = 0.0

# 🏎️ HELLCAT PROTOCOL - PERFORMANCE MODES
PERFORMANCE_MODES = {
    "stealth": {"name": "BLACK KEY (Stealth)", "multiplier": 3.0, "color": "\033[90m"},
    "balanced": {"name": "BLUE KEY (Balanced)", "multiplier": 1.15, "color": "\033[94m"},
    "apex": {"name": "RED KEY (Apex)", "multiplier": 1.02, "color": "\033[91m"}
}

# Load persistent frozen status
FROZEN_FILE = Path("frozen_models.json")
FROZEN_IDS = []
if FROZEN_FILE.exists():
    try:
        FROZEN_IDS = json.loads(FROZEN_FILE.read_text())
    except:
        pass

MODEL_REGISTRY: List[ModelConfig] = [
    # GOOGLE (March 2026 Verified Fleet)
    ModelConfig(
        id="gemini-3.1-pro-preview", gateway="google", tier="expensive", 
        note="March 2026 Flagship Reasoning (1M Context)", rpm=360, rpd=1000, tpm=2000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-3.1-pro-preview-customtools", gateway="google", tier="expensive", 
        note="Optimized for Bash/Custom Tools", rpm=360, rpd=1000, tpm=2000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-3-flash-preview", gateway="google", tier="cheap", 
        note="Vibe Coding & Multimodal Understanding", rpm=2000, rpd=10000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-3.1-flash-lite-preview", gateway="google", tier="free", 
        note="High-Volume Agentic Efficiency", rpm=4000, rpd=150000, tpm=4000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-3.1-flash-image-preview", gateway="google", tier="expensive", 
        note="Nano Banana 2 (Audio/Visual Generation)", rpm=100, rpd=1000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-3-pro-image-preview", gateway="google", tier="expensive", 
        note="Nano Banana Pro (Professional Creative Engine)", rpm=100, rpd=1000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-2.5-pro", gateway="google", tier="expensive", 
        note="Stable Flagship Reasoning", rpm=360, rpd=1000, tpm=2000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-2.5-flash", gateway="google", tier="cheap", 
        note="Stable Production Workhorse", rpm=2000, rpd=10000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-2.5-flash-lite", gateway="google", tier="free", 
        note="Stable Efficiency Leader", rpm=4000, rpd=150000, tpm=4000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-2.5-flash-image", gateway="google", tier="cheap", 
        note="Stable Visual Creator", rpm=500, rpd=5000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="gemini-2.0-flash", gateway="google", tier="free", 
        note="Generative Speed Specialist", rpm=4000, rpd=999999, tpm=4000000,
        status="active"
    ),
    ModelConfig(
        id="lyria-3-clip-preview", gateway="google", tier="expensive", 
        note="Music Generation Specialist", rpm=10, rpd=100, tpm=100000,
        status="active"
    ),

    # GROQ / OSS FRONTIER
    ModelConfig(
        id="meta-llama/llama-4-scout-17b-16e-instruct", gateway="groq", tier="free", 
        note="Llama 4 Frontier Scout (March 2026 Build)", rpm=2000, rpd=10000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="openai/gpt-oss-120b", gateway="groq", tier="expensive", 
        note="OpenAI GPT-OSS Flagship (Self-Hosted)", rpm=300, rpd=5000, tpm=500000,
        status="active"
    ),
    ModelConfig(
        id="openai/gpt-oss-20b", gateway="groq", tier="cheap", 
        note="OpenAI GPT-OSS High-Speed", rpm=1000, rpd=10000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="openai/gpt-oss-safeguard-20b", gateway="groq", tier="free", 
        note="GPT-OSS Alignment Safety Wrapper", rpm=1000, rpd=10000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="llama-3.3-70b-versatile", gateway="groq", tier="cheap", 
        note="Standard Production Logic (Llama 3.3)", rpm=1000, rpd=10000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="llama-3.1-8b-instant", gateway="groq", tier="free", 
        note="Ultra-Fast Latency Leader", rpm=5000, rpd=100000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="allam-2-7b", gateway="groq", tier="free", 
        note="Highly Optimized Compact Reasoner", rpm=3000, rpd=50000, tpm=2000000,
        status="active"
    ),
    ModelConfig(
        id="moonshotai/kimi-k2-instruct-0905", gateway="groq", tier="expensive", 
        note="Kimi K2 Long-Context Flagship", rpm=100, rpd=1000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="moonshotai/kimi-k2-instruct", gateway="groq", tier="expensive", 
        note="Kimi K2 Base Instruct", rpm=100, rpd=1000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="qwen/qwen3-32b", gateway="groq", tier="cheap", 
        note="Alibaba qwen3 (32B) High-Logic Agent", rpm=500, rpd=5000, tpm=500000,
        status="active"
    ),
    ModelConfig(
        id="groq/compound", gateway="groq", tier="expensive", 
        note="Groq Compound Reasoner (Ultra-Fast)", rpm=200, rpd=2000, tpm=200000,
        status="active"
    ),
    ModelConfig(
        id="groq/compound-mini", gateway="groq", tier="cheap", 
        note="Groq Optimized Mini", rpm=1000, rpd=10000, tpm=1000000,
        status="active"
    ),
    ModelConfig(
        id="meta-llama/llama-prompt-guard-2-86m", gateway="groq", tier="free", 
        note="Llama Prompt Guard (86M)", rpm=5000, rpd=100000, tpm=5000000,
        status="active"
    ),
    ModelConfig(
        id="meta-llama/llama-prompt-guard-2-22m", gateway="groq", tier="free", 
        note="Llama Prompt Guard (22M)", rpm=5000, rpd=100000, tpm=5000000,
        status="active"
    ),
    
    # DEEPSEEK & MISTRAL
    ModelConfig(
        id="deepseek-chat", gateway="deepseek", tier="cheap", 
        note="DeepSeek V3 (Standard Chat)", rpm=100, rpd=1000, tpm=100000,
        status="active"
    ),
    ModelConfig(
        id="deepseek-reasoner", gateway="deepseek", tier="expensive", 
        note="DeepSeek R1 (Reinforcement Logic)", rpm=100, rpd=1000, tpm=100000,
        status="active"
    ),
    ModelConfig(
        id="mistral-large-latest", gateway="mistral", tier="expensive", 
        note="Mistral Large 2 (Creative Reasoning)", rpm=100, rpd=1000, tpm=100000,
        status="active"
    )
]

# Apply Status Overrides
for m in MODEL_REGISTRY:
    if m.id in FROZEN_IDS:
        m.status = "frozen"
