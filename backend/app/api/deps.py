from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models import User
from app.core.security import decode_access_token
from sqlalchemy.future import select

async def get_current_user(
    access_token: str = Cookie(None),
    session: AsyncSession = Depends(get_session)
):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_id = decode_access_token(access_token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user
