from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import session_dependency
from app.services.workflow import (
    initialize_contract_receivable_and_delivery,
    opportunity_to_contract,
    visit_to_opportunity,
)


def build_workflow_router(session_factory) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["workflows"])
    get_session = session_dependency(session_factory)

    @router.post("/visits/{visit_id}/convert-to-opportunity")
    def convert_visit(visit_id: int, session: Session = Depends(get_session)) -> dict:
        return visit_to_opportunity(session, visit_id)

    @router.post("/opportunities/{opportunity_id}/convert-to-contract")
    def convert_opportunity(opportunity_id: int, session: Session = Depends(get_session)) -> dict:
        return opportunity_to_contract(session, opportunity_id)

    @router.post("/contracts/{contract_id}/initialize-receivable-and-delivery")
    def initialize_contract(contract_id: int, session: Session = Depends(get_session)) -> dict:
        return initialize_contract_receivable_and_delivery(session, contract_id)

    return router
