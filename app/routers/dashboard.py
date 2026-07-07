from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import session_dependency
from app.services.metrics import dashboard_summary


def build_dashboard_router(session_factory) -> APIRouter:
    router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
    get_session = session_dependency(session_factory)

    @router.get("/summary")
    def summary(session: Session = Depends(get_session)) -> dict:
        return dashboard_summary(session)

    return router
