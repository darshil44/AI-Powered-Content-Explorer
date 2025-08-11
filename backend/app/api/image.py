from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.mcp.client import MCPClient
from app.core.config import settings
from app.core.redis import get_redis
from app import models, schemas
import json

router = APIRouter(prefix="/image", tags=["image"])

@router.post("/", response_model=schemas.ImageGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_image(
    payload: schemas.ImageGenerateRequest,
    session: AsyncSession = Depends(get_session),
    redis=Depends(get_redis),
    current_user: models.User = Depends(get_current_user),
):
    prompt = payload.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Prompt must not be empty")

    cache_key = f"mcp:image:{current_user.id}:{prompt}"
    cached = await redis.get(cache_key)
    if cached:
        cached_data = json.loads(cached)
        return {
            "cached": True,
            "image_url": cached_data["image_url"],
            "saved_id": cached_data.get("saved_id"),
        }

    client = MCPClient(
        base_url=settings.FLUX_MCP_URL,
        api_key=settings.FLUX_API_KEY
    )

    try:
        response = await client.call_tool("generateImageUrl", {"prompt": prompt})
        image_url = response.get("result", {}).get("url")
        if not image_url:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="MCP Image server returned invalid response")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"MCP server error: {str(e)}")

    new_entry = models.ImageHistory(
        user_id=current_user.id,
        prompt=prompt,
        image_url=image_url,
        mcp_response=response,
        mcp_server=settings.FLUX_MCP_URL,
    )
    session.add(new_entry)
    await session.commit()
    await session.refresh(new_entry)

    await redis.set(
        cache_key,
        json.dumps({"image_url": image_url, "saved_id": str(new_entry.id)}),
        ex=300,
    )

    return {
        "cached": False,
        "image_url": image_url,
        "saved_id": str(new_entry.id),
    }