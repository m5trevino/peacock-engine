import httpx
try:
    from pydantic_ai.providers.groq import GroqProvider
    from pydantic_ai.models.groq import GroqModel
    print("✅ Groq Modules Imported")
except ImportError as e:
    print(f"❌ Groq Import Failed: {e}")

try:
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.models.openai import OpenAIModel
    print("✅ OpenAI Modules Imported")
except ImportError as e:
    print(f"❌ OpenAI Import Failed: {e}")

try:
    from pydantic_ai.providers.google import GoogleProvider
    from pydantic_ai.models.google import GoogleModel
    print("✅ Google Modules Imported (GoogleModel)")
except ImportError as e:
    print(f"⚠️ GoogleModel Import Failed: {e}")
    try:
        from pydantic_ai.models.gemini import GeminiModel
        print("ℹ️ Fallback to GeminiModel")
    except ImportError as e2:
        print(f"❌ GeminiModel Import Failed: {e2}")

# Test Instantiation
http_client = httpx.AsyncClient()
api_key = "mock_key"

print("\n--- Testing Groq ---")
try:
    provider = GroqProvider(api_key=api_key, http_client=http_client)
    model = GroqModel("llama-3.1", provider=provider)
    print("✅ Groq Instantiated")
except Exception as e:
    print(f"❌ Groq Failed: {e}")

print("\n--- Testing OpenAI ---")
try:
    provider = OpenAIProvider(api_key=api_key, http_client=http_client)
    model = OpenAIModel("gpt-4", provider=provider)
    print("✅ OpenAI Instantiated")
except Exception as e:
    print(f"❌ OpenAI Failed: {e}")

print("\n--- Testing Google ---")
try:
    provider = GoogleProvider(api_key=api_key, http_client=http_client)
    try:
        from pydantic_ai.models.google import GoogleModel
        model = GoogleModel("gemini-1.5-flash", provider=provider)
        print("✅ GoogleModel Instantiated")
    except ImportError:
        # Check if GeminiModel works with GoogleProvider (unlikely per analysis, but testing)
        from pydantic_ai.models.gemini import GeminiModel
        model = GeminiModel("gemini-1.5-flash", provider=provider)
        print("✅ GeminiModel Instantiated with GoogleProvider")
except Exception as e:
    print(f"❌ Google Failed: {e}")
