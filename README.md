# 🧠 PEACOCK ENGINE (AI-HANDLER)
**Headless AI Orchestrator & Key Rotator**

## 💀 THE MISSION
The central nervous system. It decouples the UI from the API keys. It handles the "dirty work" of contacting Google Gemini, Groq, Mistral, and Deepseek, managing rate limits, and normalizing responses.

## 🏗️ ARCHITECTURE
*   **Runtime:** Node.js (TypeScript) + Express.
*   **Security:** `KeyManager.ts` implements Round-Robin key rotation.
*   **Storage:** Local Filesystem access for "Ammo" (Context files) and "Prompts".

## 🚀 PROTOCOLS
### 1. Ignite Engine
`npm run dev`
*Port:* `8888`

## 🛠️ FEATURES
*   **Universal Striker:** Single endpoint (`/v1/strike`) for all models.
*   **Key Pools:** Automatic failover if a key is rate-limited.
*   **Model Registry:** Centralized configuration for model Tiers (Cheap vs Expensive).
