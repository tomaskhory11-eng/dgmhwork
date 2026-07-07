from __future__ import annotations

from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import to_dict
from app.models import Contract, DeliveryProject, Opportunity, Receivable, Visit
from app.services.audit_log import write_audit_log


def visit_to_opportunity(session: Session, visit_id: int) -> dict:
    visit = session.get(Visit, visit_id)
    if visit is None:
        raise HTTPException(status_code=404, detail="visit not found")
    if visit.opportunity_id:
        existing = session.get(Opportunity, visit.opportunity_id)
        if existing is not None:
            return to_dict(existing)

    opportunity = Opportunity(
        project_name=visit.related_project or f"{visit.customer_name}商机",
        customer_name=visit.customer_name,
        business_segment=visit.business_detail,
        business_detail=visit.business_detail,
        project_source="客户拜访",
        project_stage="需求沟通",
        estimated_contract_amount=visit.estimated_amount,
        is_key_project=False,
        business_owner=visit.business_owner,
        latest_follow_date=visit.visit_date,
        follow_status=visit.next_action,
        remark=visit.key_notes,
    )
    session.add(opportunity)
    session.flush()
    visit.is_opportunity = True
    visit.opportunity_id = opportunity.id
    write_audit_log(
        session,
        entity_type="opportunities",
        entity_id=opportunity.id,
        action="create",
        summary=f"由拜访记录 {visit.id} 转为储备项目",
    )
    session.commit()
    session.refresh(opportunity)
    return to_dict(opportunity)


def opportunity_to_contract(session: Session, opportunity_id: int) -> dict:
    opportunity = session.get(Opportunity, opportunity_id)
    if opportunity is None:
        raise HTTPException(status_code=404, detail="opportunity not found")
    if opportunity.contract_id:
        existing = session.get(Contract, opportunity.contract_id)
        if existing is not None:
            return to_dict(existing)

    contract = Contract(
        application_date=date.today(),
        contract_name=opportunity.project_name,
        customer_name=opportunity.customer_name,
        customer_category=opportunity.customer_category,
        region=opportunity.city or opportunity.province,
        business_segment=opportunity.business_segment,
        business_detail=opportunity.business_detail,
        business_owner=opportunity.business_owner,
        contract_amount=opportunity.estimated_contract_amount,
        is_key_project=opportunity.is_key_project,
        remark=opportunity.remark,
    )
    session.add(contract)
    session.flush()
    opportunity.is_converted = True
    opportunity.project_stage = "已签约"
    opportunity.contract_id = contract.id
    write_audit_log(
        session,
        entity_type="contracts",
        entity_id=contract.id,
        action="create",
        summary=f"由储备项目 {opportunity.id} 转为合同",
    )
    session.commit()
    session.refresh(contract)
    return to_dict(contract)


def initialize_contract_receivable_and_delivery(session: Session, contract_id: int) -> dict:
    contract = session.get(Contract, contract_id)
    if contract is None:
        raise HTTPException(status_code=404, detail="contract not found")

    receivable = None
    delivery_project = None
    if not contract.receivable_initialized:
        receivable = Receivable(
            contract_number=contract.contract_number,
            customer_name=contract.customer_name,
            project_name=contract.contract_name,
            contract_amount=contract.contract_amount,
            total_outstanding=contract.contract_amount,
            collectible_amount=contract.contract_amount,
            payment_condition=contract.payment_method,
            contract_due_date=contract.contract_due_date,
            planned_payment_amount=contract.contract_amount,
            business_owner=contract.business_owner,
        )
        session.add(receivable)
        session.flush()
        contract.receivable_initialized = True
        write_audit_log(
            session,
            entity_type="receivables",
            entity_id=receivable.id,
            action="create",
            summary=f"由合同 {contract.id} 初始化应收",
        )
    else:
        receivable = (
            session.query(Receivable)
            .filter(Receivable.project_name == contract.contract_name, Receivable.customer_name == contract.customer_name)
            .order_by(Receivable.id.desc())
            .first()
        )

    if not contract.delivery_initialized:
        delivery_project = DeliveryProject(
            project_name=contract.contract_name,
            contract_number=contract.contract_number,
            customer_name=contract.customer_name,
            business_type=contract.business_detail or contract.business_segment,
            project_owner=contract.business_owner,
            delivery_stage="待启动",
            current_progress="合同已确认，待制定实施计划",
        )
        session.add(delivery_project)
        session.flush()
        contract.delivery_initialized = True
        write_audit_log(
            session,
            entity_type="delivery-projects",
            entity_id=delivery_project.id,
            action="create",
            summary=f"由合同 {contract.id} 初始化实施项目",
        )
    else:
        delivery_project = (
            session.query(DeliveryProject)
            .filter(DeliveryProject.project_name == contract.contract_name, DeliveryProject.customer_name == contract.customer_name)
            .order_by(DeliveryProject.id.desc())
            .first()
        )

    session.commit()
    if receivable is not None:
        session.refresh(receivable)
    if delivery_project is not None:
        session.refresh(delivery_project)
    return {
        "receivable": to_dict(receivable) if receivable is not None else None,
        "delivery_project": to_dict(delivery_project) if delivery_project is not None else None,
    }
