from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class DashboardFilter(BaseModel):
    type: Optional[Literal["search", "image"]] = None
    keyword: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class SearchEntry(BaseModel):
    id: str
    query: str
    mcp_response: dict
    mcp_server: str
    created_at: datetime

    class Config:
        orm_mode = True

class ImageEntry(BaseModel):
    id: str
    prompt: str
    image_url: str
    mcp_response: dict
    mcp_server: str
    created_at: datetime

    class Config:
        orm_mode = True

class DashboardResponse(BaseModel):
    searches: List[SearchEntry] = []
    images: List[ImageEntry] = []
