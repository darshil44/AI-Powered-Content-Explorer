from pydantic import BaseModel
from typing import Any, Optional

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    cached: bool
    result: Any
    saved_id: Optional[str]
