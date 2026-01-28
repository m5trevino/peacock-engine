from pydantic import BaseModel
from typing import List, Literal

class ModelConfig(BaseModel):
    id: str
    gateway: Literal['groq', 'google', 'deepseek', 'mistral']
    tier: Literal['free', 'cheap', 'expensive', 'custom']
    note: str

MODEL_REGISTRY: List[ModelConfig] = [
    # GROQ
    ModelConfig(id="llama-3.3-70b-versatile", gateway="groq", tier="expensive", note="Meta Llama 3.3 70B"),
    ModelConfig(id="llama-3.1-8b-instant", gateway="groq", tier="free", note="Meta Llama 3.1 8B"),
    ModelConfig(id="meta-llama/llama-4-maverick-17b-128e-instruct", gateway="groq", tier="expensive", note="Llama 4 Maverick (17B)"),
    ModelConfig(id="meta-llama/llama-4-scout-17b-16e-instruct", gateway="groq", tier="expensive", note="Llama 4 Scout (17B)"),
    ModelConfig(id="groq/compound", gateway="groq", tier="expensive", note="Groq Compound"),
    ModelConfig(id="groq/compound-mini", gateway="groq", tier="cheap", note="Groq Compound Mini"),
    ModelConfig(id="openai/gpt-oss-120b", gateway="groq", tier="expensive", note="OpenAI GPT-OSS 120B"),
    ModelConfig(id="openai/gpt-oss-20b", gateway="groq", tier="cheap", note="OpenAI GPT-OSS 20B"),
    ModelConfig(id="openai/gpt-oss-safeguard-20b", gateway="groq", tier="cheap", note="OpenAI GPT-OSS Safeguard 20B"),
    ModelConfig(id="moonshotai/kimi-k2-instruct", gateway="groq", tier="expensive", note="Moonshot Kimi K2"),
    ModelConfig(id="moonshotai/kimi-k2-instruct-0905", gateway="groq", tier="expensive", note="Moonshot Kimi K2 (0905)"),
    ModelConfig(id="qwen/qwen3-32b", gateway="groq", tier="cheap", note="Qwen 3 32B"),
    ModelConfig(id="allam-2-7b", gateway="groq", tier="free", note="SDAIA Allam 2 (Arabic)"),

    # DEEPSEEK
    ModelConfig(id="deepseek-reasoner", gateway="deepseek", tier="expensive", note="DeepSeek R1 (Reasoning)"),
    ModelConfig(id="deepseek-chat", gateway="deepseek", tier="cheap", note="DeepSeek V3 (Chat)"),

    # MISTRAL
    ModelConfig(id="mistral-large-latest", gateway="mistral", tier="expensive", note="Mistral Large"),
    ModelConfig(id="mistral-medium-latest", gateway="mistral", tier="expensive", note="Mistral Medium"),
    ModelConfig(id="mistral-small-latest", gateway="mistral", tier="cheap", note="Mistral Small"),
    ModelConfig(id="pixtral-large-latest", gateway="mistral", tier="expensive", note="Pixtral Large"),
    ModelConfig(id="pixtral-12b-latest", gateway="mistral", tier="cheap", note="Pixtral 12B"),
    ModelConfig(id="codestral-latest", gateway="mistral", tier="expensive", note="Codestral (Latest)"),
    ModelConfig(id="codestral-2501", gateway="mistral", tier="expensive", note="Codestral 2501"),
    ModelConfig(id="ministral-14b-latest", gateway="mistral", tier="cheap", note="Ministral 14B"),
    ModelConfig(id="ministral-8b-latest", gateway="mistral", tier="cheap", note="Ministral 8B"),
    ModelConfig(id="ministral-3b-latest", gateway="mistral", tier="free", note="Ministral 3B"),
    ModelConfig(id="magistral-medium-latest", gateway="mistral", tier="expensive", note="Magistral Medium (Reasoning)"),
    ModelConfig(id="magistral-small-latest", gateway="mistral", tier="cheap", note="Magistral Small"),
    ModelConfig(id="devstral-2512", gateway="mistral", tier="cheap", note="Devstral 2512"),
    ModelConfig(id="labs-mistral-small-creative", gateway="mistral", tier="cheap", note="Mistral Small Creative"),
    ModelConfig(id="open-mistral-nemo", gateway="mistral", tier="cheap", note="Mistral Nemo"),

    # GOOGLE
    ModelConfig(id="models/gemini-3-pro-preview", gateway="google", tier="expensive", note="Gemini 3 Pro"),
    ModelConfig(id="models/gemini-3-flash-preview", gateway="google", tier="cheap", note="Gemini 3 Flash"),
    ModelConfig(id="models/deep-research-pro-preview-12-2025", gateway="google", tier="expensive", note="Deep Research Pro"),
    ModelConfig(id="models/gemini-2.5-pro", gateway="google", tier="expensive", note="Gemini 2.5 Pro"),
    ModelConfig(id="models/gemini-2.0-flash", gateway="google", tier="cheap", note="Gemini 2.0 Flash"),
    ModelConfig(id="models/gemini-exp-1206", gateway="google", tier="expensive", note="Gemini Exp 1206"),
]
