from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.mcp.client import MCPClient
from app.core.config import settings
from app.core.redis import get_redis
from app import models, schemas
from app.api.deps import get_current_user
import json

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/", response_model=schemas.SearchResponse)
async def do_search(
    payload: schemas.SearchRequest,
    session: AsyncSession = Depends(get_session),
    redis=Depends(get_redis),
    current_user: models.User = Depends(get_current_user),
):
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Query cannot be empty")

    cache_key = f"mcp:search:{current_user.id}:{query}"
    cached = await redis.get(cache_key)
    if cached:
        result = json.loads(cached)
        return {"cached": True, "result": result}

    client = MCPClient(
        settings.TAVILY_MCP_URL,
        api_key=settings.TAVILY_API_KEY,
        profile=settings.TAVILY_PROFILE
    )

    try:
        response = await client.call_tool("tavily-search", {"query": query, "limit": 5})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"MCP Server error: {str(e)}")

    entry = models.SearchHistory(user_id=current_user.id, query=query, mcp_response=response, mcp_server=settings.TAVILY_MCP_URL)
    session.add(entry)
    await session.commit()
    await session.refresh(entry)

    await redis.set(cache_key, json.dumps(response), ex=300)

    return {"cached": False, "result": response, "saved_id": str(entry.id)}