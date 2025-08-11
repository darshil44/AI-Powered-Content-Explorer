from typing import Optional, List
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB, TIMESTAMP, TEXT as PG_TEXT, INTEGER
import uuid
from datetime import datetime, timedelta

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True),
    email: str = Field(nullable=False, unique=True, index=True, max_length=255),
    hashed_password: str = Field(nullable=False),
    is_active: bool = Field(default=True),
    is_admin: bool = Field(default=False),
    created_at: datetime = Field(default_factory=datetime.utcnow),
server_default=text('now()')


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    user_id: uuid.UUID = Field(sa_column=Column(PG_UUID(as_uuid=True), nullable=False))
    token_hash: str = Field(sa_column=Column(PG_TEXT, nullable=False))
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=30), sa_column=Column(TIMESTAMP(timezone=True)))

class SearchHistory(SQLModel, table=True):
    __tablename__ = "search_history"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, sa_column=Column(PG_UUID(as_uuid=True), primary_key=True))
    user_id: uuid.UUID = Field(sa_column=Column(PG_UUID(as_uuid=True), nullable=False))
    query: str
    mcp_response: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    mcp_server: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), server_default=text('now()')))

class ImageHistory(SQLModel, table=True):
    __tablename__ = "image_history"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", index=True)
    prompt: str = Field(nullable=False, max_length=500)
    image_url: str = Field(nullable=False)
    mcp_response: dict = Field(sa_column=Column(JSONB), nullable=False)
    mcp_server: str = Field(nullable=False, max_length=256)
    created_at: datetime = Field(default_factory=datetime.utcnow)

