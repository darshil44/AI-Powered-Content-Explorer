import uvicorn
from fastapi import FastAPI
from app.api import auth, search
from app.db.session import init_db
from app.core.config import settings
import redis.asyncio as aioredis

app = FastAPI(title="AI Content Explorer Backend")

app.include_router(auth.router)
app.include_router(search.router)

@app.on_event("startup")
async def on_startup():
    # create db tables if missing
    await init_db()
    # init redis client and attach to app state
    app.state.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

@app.on_event("shutdown")
async def on_shutdown():
    if getattr(app.state, "redis", None):
        await app.state.redis.close()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
