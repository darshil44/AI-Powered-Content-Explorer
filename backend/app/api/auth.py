from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas import auth as auth_schemas
from app.models import User
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from sqlalchemy.future import select
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

@router.post("/register", response_model=auth_schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(payload: auth_schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    # Check if user exists
    result = await session.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(payload: auth_schemas.UserCreate, response: Response, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)

    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,  # Set True if HTTPS
        samesite="lax",
        path="/",
    )
    return {"message": "Login successful"}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "Logout successful"}

@router.get("/me", response_model=auth_schemas.UserRead)
async def get_current_user(access_token: str = Cookie(None), session: AsyncSession = Depends(get_session)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decode_access_token(access_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
