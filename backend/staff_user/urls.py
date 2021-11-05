from fastapi import APIRouter

from staff_user.views import es_view

es_router = APIRouter()

es_router.include_router( es_view.router,prefix="/es", tags=["es"])