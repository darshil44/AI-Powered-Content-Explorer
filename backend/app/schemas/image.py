from pydantic import BaseModel, Field
from typing import Optional

class ImageGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500, description="Text prompt for AI image generation")

class ImageGenerateResponse(BaseModel):
    cached: bool
    image_url: str
    saved_id: Optional[str] = None
