from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from typing import Optional
from datetime import datetime

from app.db.session import get_session
from app.api.deps import get_current_user
from app.models import SearchHistory, ImageHistory, User
from app.schemas import dashboard as dashboard_schemas

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=dashboard_schemas.DashboardResponse)
async def get_dashboard_entries(
    type: Optional[str] = Query(None, regex="^(search|image)$"),
    keyword: Optional[str] = Query(None, min_length=1),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    filters_search = [SearchHistory.user_id == current_user.id]
    filters_image = [ImageHistory.user_id == current_user.id]

    if keyword:
        filters_search.append(SearchHistory.query.ilike(f"%{keyword}%"))
        filters_image.append(ImageHistory.prompt.ilike(f"%{keyword}%"))

    if date_from:
        filters_search.append(SearchHistory.created_at >= date_from)
        filters_image.append(ImageHistory.created_at >= date_from)

    if date_to:
        filters_search.append(SearchHistory.created_at <= date_to)
        filters_image.append(ImageHistory.created_at <= date_to)

    searches = []
    images = []

    if type in (None, "search"):
        result = await session.execute(select(SearchHistory).where(and_(*filters_search)).order_by(SearchHistory.created_at.desc()).limit(50))
        searches = result.scalars().all()

    if type in (None, "image"):
        result = await session.execute(select(ImageHistory).where(and_(*filters_image)).order_by(ImageHistory.created_at.desc()).limit(50))
        images = result.scalars().all()

    return dashboard_schemas.DashboardResponse(searches=searches, images=images)

@router.delete("/search/{search_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_search_entry(
    search_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(select(SearchHistory).where(SearchHistory.id == search_id, SearchHistory.user_id == current_user.id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Search entry not found")
    await session.delete(entry)
    await session.commit()
    return

@router.delete("/image/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_entry(
    image_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(select(ImageHistory).where(ImageHistory.id == image_id, ImageHistory.user_id == current_user.id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Image entry not found")
    await session.delete(entry)
    await session.commit()
    return
