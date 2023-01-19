from fastapi import APIRouter
from .endpoints.predict import router as predict_router
from .endpoints.fetch import router as fetch_router

router = APIRouter()
router.include_router(predict_router)
router.include_router(fetch_router)
