from fastapi import APIRouter


from app.api import auth
from app.api import search
from app.api import image
from app.api import dashboard  

api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(search.router)
api_router.include_router(image.router)
api_router.include_router(dashboard.router)
