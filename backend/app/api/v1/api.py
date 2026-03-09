"""
API Router - combines all endpoint routers
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, suspects, cases, sketches, recognition

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(suspects.router, prefix="/suspects", tags=["Suspects"])
api_router.include_router(cases.router, prefix="/cases", tags=["Cases"])
api_router.include_router(sketches.router, prefix="/sketches", tags=["Sketches"])
api_router.include_router(recognition.router, prefix="/recognition", tags=["Face Recognition"])
