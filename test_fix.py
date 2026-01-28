import os
import httpx
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
# from pydantic_ai.models.gemini import GeminiModel

# Mock data
api_key = "mock_key"
http_client = httpx.AsyncClient()

print("--- Testing GroqModel Fix ---")
try:
    from groq import AsyncGroq
    client = AsyncGroq(api_key=api_key, http_client=http_client)
    model = GroqModel("llama3-8b-8192", provider=client)
    print("SUCCESS: GroqModel accepted AsyncGroq client")
except ImportError:
    print("SKIPPED: groq package not found")
except Exception as e:
    print(f"FAILED: {e}")

print("\n--- Testing OpenAIModel Fix ---")
try:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=api_key, http_client=http_client, base_url="https://api.deepseek.com")
    model = OpenAIModel("deepseek-chat", provider=client)
    print("SUCCESS: OpenAIModel accepted AsyncOpenAI client")
except ImportError:
    print("SKIPPED: openai package not found")
except Exception as e:
    print(f"FAILED: {e}")
