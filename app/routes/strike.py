from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.striker import execute_strike
from app.config import MODEL_REGISTRY

router = APIRouter()

class StrikeRequest(BaseModel):
    modelId: str
    prompt: str
    temp: Optional[float] = 0.7
    format_mode: Optional[str] = None

@router.post("")
async def strike(request: StrikeRequest):
    print(f"[DEBUG] STRIKE REQUEST RECEIVED: {request.modelId} (FMT: {request.format_mode})")
    try:
        model_config = next((m for m in MODEL_REGISTRY if m.id == request.modelId), None)
        if not model_config:
            raise HTTPException(status_code=400, detail="Unknown Model ID")
    
        result = await execute_strike(
            gateway=model_config.gateway,
            model_id=request.modelId,
            prompt=request.prompt,
            temp=request.temp,
            format_mode=request.format_mode
        )
        return result
    except Exception as e:
        print(f"[❌ STRIKE ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
