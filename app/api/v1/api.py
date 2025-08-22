"""
API v1 router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, performance_cycles, reviewer_selections, feedback_forms, notifications

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(performance_cycles.router, prefix="/performance-cycles", tags=["Performance Cycles"])
api_router.include_router(reviewer_selections.router, prefix="/reviewer-selections", tags=["Reviewer Selections"])
api_router.include_router(feedback_forms.router, prefix="/feedback-forms", tags=["Feedback Forms"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
