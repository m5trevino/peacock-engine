import inspect
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel

print("--- GroqModel ---")
try:
    print(inspect.signature(GroqModel.__init__))
except Exception as e:
    print(e)

print("\n--- OpenAIModel ---")
try:
    print(inspect.signature(OpenAIModel.__init__))
except Exception as e:
    print(e)

print("\n--- GeminiModel ---")
try:
    print(inspect.signature(GeminiModel.__init__))
except Exception as e:
    print(e)
