// ============================================================
// ⚡ PEACOCK MODEL REGISTRY (OMEGA TIER)
// ============================================================
// FULL ARSENAL: GROQ + DEEPSEEK + MISTRAL + GOOGLE
// FILTERED: Text-Generation Only (No Audio/Embed/OCR)
// ============================================================

export interface ModelConfig {
  id: string;
  gateway: 'groq' | 'google' | 'deepseek' | 'mistral';
  tier: 'free' | 'cheap' | 'expensive' | 'custom';
  note: string;
}

export const MODEL_REGISTRY: ModelConfig[] = [
  // ==========================================================
  // 1. GROQ ARSENAL (VELOCITY)
  // ==========================================================
  { id: "llama-3.3-70b-versatile", gateway: "groq", tier: "expensive", note: "Meta Llama 3.3 70B" },
  { id: "llama-3.1-8b-instant", gateway: "groq", tier: "free", note: "Meta Llama 3.1 8B" },
  { id: "meta-llama/llama-4-maverick-17b-128e-instruct", gateway: "groq", tier: "expensive", note: "Llama 4 Maverick (17B)" },
  { id: "meta-llama/llama-4-scout-17b-16e-instruct", gateway: "groq", tier: "expensive", note: "Llama 4 Scout (17B)" },
  { id: "groq/compound", gateway: "groq", tier: "expensive", note: "Groq Compound" },
  { id: "groq/compound-mini", gateway: "groq", tier: "cheap", note: "Groq Compound Mini" },
  { id: "openai/gpt-oss-120b", gateway: "groq", tier: "expensive", note: "OpenAI GPT-OSS 120B" },
  { id: "openai/gpt-oss-20b", gateway: "groq", tier: "cheap", note: "OpenAI GPT-OSS 20B" },
  { id: "openai/gpt-oss-safeguard-20b", gateway: "groq", tier: "cheap", note: "OpenAI GPT-OSS Safeguard 20B" },
  { id: "moonshotai/kimi-k2-instruct", gateway: "groq", tier: "expensive", note: "Moonshot Kimi K2" },
  { id: "moonshotai/kimi-k2-instruct-0905", gateway: "groq", tier: "expensive", note: "Moonshot Kimi K2 (0905)" },
  { id: "qwen/qwen3-32b", gateway: "groq", tier: "cheap", note: "Qwen 3 32B" },
  { id: "allam-2-7b", gateway: "groq", tier: "free", note: "SDAIA Allam 2 (Arabic)" },

  // ==========================================================
  // 2. DEEPSEEK ARSENAL (LOGIC)
  // ==========================================================
  { id: "deepseek-reasoner", gateway: "deepseek", tier: "expensive", note: "DeepSeek R1 (Reasoning)" },
  { id: "deepseek-chat", gateway: "deepseek", tier: "cheap", note: "DeepSeek V3 (Chat)" },

  // ==========================================================
  // 3. MISTRAL ARSENAL (FRONTIER)
  // ==========================================================
  // --- FLAGGSHIPS ---
  { id: "mistral-large-latest", gateway: "mistral", tier: "expensive", note: "Mistral Large" },
  { id: "mistral-medium-latest", gateway: "mistral", tier: "expensive", note: "Mistral Medium" },
  { id: "mistral-small-latest", gateway: "mistral", tier: "cheap", note: "Mistral Small" },
  
  // --- PIXTRAL (VISION/TEXT) ---
  { id: "pixtral-large-latest", gateway: "mistral", tier: "expensive", note: "Pixtral Large" },
  { id: "pixtral-12b-latest", gateway: "mistral", tier: "cheap", note: "Pixtral 12B" },

  // --- CODESTRAL (CODING) ---
  { id: "codestral-latest", gateway: "mistral", tier: "expensive", note: "Codestral (Latest)" },
  { id: "codestral-2501", gateway: "mistral", tier: "expensive", note: "Codestral 2501" },

  // --- MINISTRAL (EDGE) ---
  { id: "ministral-14b-latest", gateway: "mistral", tier: "cheap", note: "Ministral 14B" },
  { id: "ministral-8b-latest", gateway: "mistral", tier: "cheap", note: "Ministral 8B" },
  { id: "ministral-3b-latest", gateway: "mistral", tier: "free", note: "Ministral 3B" },

  // --- DEVSTRAL / MAGISTRAL (EXPERIMENTAL) ---
  { id: "magistral-medium-latest", gateway: "mistral", tier: "expensive", note: "Magistral Medium (Reasoning)" },
  { id: "magistral-small-latest", gateway: "mistral", tier: "cheap", note: "Magistral Small" },
  { id: "devstral-2512", gateway: "mistral", tier: "cheap", note: "Devstral 2512" },
  { id: "labs-mistral-small-creative", gateway: "mistral", tier: "cheap", note: "Mistral Small Creative" },
  { id: "open-mistral-nemo", gateway: "mistral", tier: "cheap", note: "Mistral Nemo" },

  // ==========================================================
  // 4. GOOGLE ARSENAL (CONTEXT)
  // ==========================================================
  { id: "models/gemini-3-pro-preview", gateway: "google", tier: "expensive", note: "Gemini 3 Pro" },
  { id: "models/gemini-3-flash-preview", gateway: "google", tier: "cheap", note: "Gemini 3 Flash" },
  { id: "models/deep-research-pro-preview-12-2025", gateway: "google", tier: "expensive", note: "Deep Research Pro" },
  { id: "models/gemini-2.5-pro", gateway: "google", tier: "expensive", note: "Gemini 2.5 Pro" },
  { id: "models/gemini-2.0-flash", gateway: "google", tier: "cheap", note: "Gemini 2.0 Flash" },
  { id: "models/gemini-exp-1206", gateway: "google", tier: "expensive", note: "Gemini Exp 1206" }
];
