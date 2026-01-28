from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.strike import router as strike_router
from app.routes.models import router as models_router
from app.routes.fs import router as fs_router

app = FastAPI(title="PEACOCK ENGINE V2 (PYTHON)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(strike_router, prefix="/v1/strike", tags=["STRIKE"])
app.include_router(models_router, prefix="/v1/models", tags=["MODELS"])
app.include_router(fs_router, prefix="/v1/fs", tags=["FILESYSTEM"])

@app.get("/health")
async def health():
    from app.core.key_manager import GroqPool, GooglePool, DeepSeekPool, MistralPool
    return {
        "status": "ONLINE", 
        "system": "PEACOCK_ENGINE_V2_PYTHON",
        "integrity": {
            "groq": len(GroqPool.deck),
            "google": len(GooglePool.deck),
            "deepseek": len(DeepSeekPool.deck),
            "mistral": len(MistralPool.deck)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3099)
