from fastapi import APIRouter
from app.api.routes.movies_routes  import movies 

router = APIRouter()

router.include_router(movies, tags=["Auth"])
