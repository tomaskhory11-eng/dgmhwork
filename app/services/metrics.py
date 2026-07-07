from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Channel, Contract, DeliveryProject, Opportunity, Payment, Receivable, Visit


def dashboard_summary(session: Session) -> dict[str, Any]:
    total_contract_amount = _sum(session, Contract.contract_amount)
    total_payment_amount = _sum(session, Payment.payment_amount)
    pipeline_amount = _sum(session, Opportunity.estimated_contract_amount, Opportunity.is_converted.is_(False))
    receivable_outstanding = _sum(session, Receivable.total_outstanding)
    key_project_count = session.scalar(select(func.count()).select_from(Opportunity).where(Opportunity.is_key_project.is_(True))) or 0
    delayed_delivery_count = (
        session.scalar(
            select(func.count())
            .select_from(DeliveryProject)
            .where(DeliveryProject.delay_reason != "")
        )
        or 0
    )

    return {
        "total_contract_amount": float(total_contract_amount),
        "total_payment_amount": float(total_payment_amount),
        "pipeline_estimated_amount": float(pipeline_amount),
        "receivable_outstanding": float(receivable_outstanding),
        "key_project_count": key_project_count,
        "delayed_delivery_count": delayed_delivery_count,
        "visit_count": session.scalar(select(func.count()).select_from(Visit)) or 0,
        "channel_count": session.scalar(select(func.count()).select_from(Channel)) or 0,
    }


def _sum(session: Session, column, *conditions) -> Decimal:
    statement = select(func.coalesce(func.sum(column), 0))
    if conditions:
        statement = statement.where(*conditions)
    value = session.scalar(statement)
    return Decimal(str(value or 0))
