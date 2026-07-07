from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TimestampMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class StatusMixin:
    status: Mapped[str] = mapped_column(String(32), default="有效")


class User(TimestampMixin, StatusMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    role: Mapped[str] = mapped_column(String(64), default="商务人员")
    username: Mapped[str] = mapped_column(String(100), unique=True)


class FieldOption(TimestampMixin, StatusMixin, Base):
    __tablename__ = "field_options"

    category: Mapped[str] = mapped_column(String(80), index=True)
    value: Mapped[str] = mapped_column(String(120), index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Customer(TimestampMixin, StatusMixin, Base):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(200), index=True)
    customer_type: Mapped[str] = mapped_column(String(120), default="")
    customer_nature: Mapped[str] = mapped_column(String(120), default="")
    industry: Mapped[str] = mapped_column(String(120), default="")
    region: Mapped[str] = mapped_column(String(120), default="")
    contact_person: Mapped[str] = mapped_column(String(120), default="")
    contact_phone: Mapped[str] = mapped_column(String(120), default="")
    customer_level: Mapped[str] = mapped_column(String(32), default="")
    owner: Mapped[str] = mapped_column(String(120), default="")


class Channel(TimestampMixin, StatusMixin, Base):
    __tablename__ = "channels"

    channel_category: Mapped[str] = mapped_column(String(120), default="")
    organization: Mapped[str] = mapped_column(String(200), index=True)
    contact_person: Mapped[str] = mapped_column(String(120), default="")
    key_resource: Mapped[str] = mapped_column(Text, default="")
    resource_type: Mapped[str] = mapped_column(String(120), default="")
    related_business: Mapped[str] = mapped_column(String(160), default="")
    cooperation_stage: Mapped[str] = mapped_column(String(120), default="")
    channel_level: Mapped[str] = mapped_column(String(32), default="")
    owner: Mapped[str] = mapped_column(String(120), default="")
    business_owner: Mapped[str] = mapped_column(String(120), default="")
    lead_count: Mapped[int] = mapped_column(Integer, default=0)
    opportunity_count: Mapped[int] = mapped_column(Integer, default=0)
    estimated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    latest_contact_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_action: Mapped[str] = mapped_column(Text, default="")


class Visit(TimestampMixin, StatusMixin, Base):
    __tablename__ = "visits"

    visit_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    customer_name: Mapped[str] = mapped_column(String(200), index=True)
    visit_target: Mapped[str] = mapped_column(String(160), default="")
    contact_info: Mapped[str] = mapped_column(String(160), default="")
    visit_purpose: Mapped[str] = mapped_column(Text, default="")
    related_project: Mapped[str] = mapped_column(String(200), default="")
    business_detail: Mapped[str] = mapped_column(String(160), default="")
    business_owner: Mapped[str] = mapped_column(String(120), default="")
    participants: Mapped[str] = mapped_column(Text, default="")
    key_notes: Mapped[str] = mapped_column(Text, default="")
    customer_attitude: Mapped[str] = mapped_column(String(80), default="")
    result: Mapped[str] = mapped_column(Text, default="")
    estimated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    next_action: Mapped[str] = mapped_column(Text, default="")
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_opportunity: Mapped[bool] = mapped_column(Boolean, default=False)
    opportunity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Opportunity(TimestampMixin, StatusMixin, Base):
    __tablename__ = "opportunities"

    project_name: Mapped[str] = mapped_column(String(240), index=True)
    customer_name: Mapped[str] = mapped_column(String(200), index=True)
    customer_level: Mapped[str] = mapped_column(String(32), default="")
    customer_category: Mapped[str] = mapped_column(String(120), default="")
    customer_nature: Mapped[str] = mapped_column(String(120), default="")
    province: Mapped[str] = mapped_column(String(80), default="")
    city: Mapped[str] = mapped_column(String(80), default="")
    business_segment: Mapped[str] = mapped_column(String(160), default="")
    business_detail: Mapped[str] = mapped_column(String(160), default="")
    project_source: Mapped[str] = mapped_column(String(120), default="")
    project_stage: Mapped[str] = mapped_column(String(80), default="线索")
    estimated_contract_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    expected_sign_month: Mapped[str] = mapped_column(String(20), default="")
    is_key_project: Mapped[bool] = mapped_column(Boolean, default=False)
    business_owner: Mapped[str] = mapped_column(String(120), default="")
    latest_follow_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    follow_status: Mapped[str] = mapped_column(String(120), default="")
    is_converted: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remark: Mapped[str] = mapped_column(Text, default="")


class GroupProject(TimestampMixin, StatusMixin, Base):
    __tablename__ = "group_projects"

    brother_company: Mapped[str] = mapped_column(String(160), default="")
    project_name: Mapped[str] = mapped_column(String(240), index=True)
    customer_name: Mapped[str] = mapped_column(String(200), default="")
    business_segment: Mapped[str] = mapped_column(String(160), default="")
    project_source: Mapped[str] = mapped_column(String(120), default="")
    project_stage: Mapped[str] = mapped_column(String(80), default="")
    estimated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    success_probability: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    weighted_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    beijing_owner: Mapped[str] = mapped_column(String(120), default="")
    branch_contact: Mapped[str] = mapped_column(String(120), default="")
    collaboration_method: Mapped[str] = mapped_column(Text, default="")
    next_action: Mapped[str] = mapped_column(Text, default="")
    planned_completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)


class Contract(TimestampMixin, StatusMixin, Base):
    __tablename__ = "contracts"

    application_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    contract_return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    contract_number: Mapped[str] = mapped_column(String(120), index=True, default="")
    contract_name: Mapped[str] = mapped_column(String(240), index=True)
    customer_name: Mapped[str] = mapped_column(String(200), index=True)
    customer_category: Mapped[str] = mapped_column(String(120), default="")
    industry_category: Mapped[str] = mapped_column(String(120), default="")
    region: Mapped[str] = mapped_column(String(120), default="")
    business_segment: Mapped[str] = mapped_column(String(160), default="")
    business_detail: Mapped[str] = mapped_column(String(160), default="")
    business_owner: Mapped[str] = mapped_column(String(120), default="")
    collaboration_unit: Mapped[str] = mapped_column(String(160), default="")
    contract_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(6, 4), default=0)
    direct_cost: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    estimated_gross_profit: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    service_period: Mapped[str] = mapped_column(String(120), default="")
    contract_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    payment_method: Mapped[str] = mapped_column(String(120), default="")
    is_key_project: Mapped[bool] = mapped_column(Boolean, default=False)
    is_group_collaboration: Mapped[bool] = mapped_column(Boolean, default=False)
    receivable_initialized: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_initialized: Mapped[bool] = mapped_column(Boolean, default=False)
    remark: Mapped[str] = mapped_column(Text, default="")


class Receivable(TimestampMixin, StatusMixin, Base):
    __tablename__ = "receivables"

    contract_number: Mapped[str] = mapped_column(String(120), index=True, default="")
    customer_name: Mapped[str] = mapped_column(String(200), index=True)
    project_name: Mapped[str] = mapped_column(String(240), index=True)
    contract_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    total_outstanding: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    collectible_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    uncollectible_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    invoiced_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    payment_condition: Mapped[str] = mapped_column(Text, default="")
    contract_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    overdue_days: Mapped[int] = mapped_column(Integer, default=0)
    collection_status: Mapped[str] = mapped_column(String(120), default="")
    planned_payment_month: Mapped[str] = mapped_column(String(20), default="")
    planned_payment_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    business_owner: Mapped[str] = mapped_column(String(120), default="")


class Payment(TimestampMixin, StatusMixin, Base):
    __tablename__ = "payments"

    arrival_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    contract_number: Mapped[str] = mapped_column(String(120), index=True, default="")
    customer_name: Mapped[str] = mapped_column(String(200), index=True)
    project_name: Mapped[str] = mapped_column(String(240), index=True)
    payment_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    payment_method: Mapped[str] = mapped_column(String(120), default="")
    remark: Mapped[str] = mapped_column(Text, default="")


class DeliveryProject(TimestampMixin, StatusMixin, Base):
    __tablename__ = "delivery_projects"

    project_name: Mapped[str] = mapped_column(String(240), index=True)
    contract_number: Mapped[str] = mapped_column(String(120), index=True, default="")
    customer_name: Mapped[str] = mapped_column(String(200), index=True)
    business_type: Mapped[str] = mapped_column(String(160), default="")
    project_owner: Mapped[str] = mapped_column(String(120), default="")
    delivery_stage: Mapped[str] = mapped_column(String(120), default="")
    planned_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    planned_completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_completion_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    current_progress: Mapped[str] = mapped_column(Text, default="")
    deliverable_files: Mapped[str] = mapped_column(Text, default="")
    customer_confirmation_status: Mapped[str] = mapped_column(String(120), default="")
    delay_reason: Mapped[str] = mapped_column(Text, default="")
    support_needed: Mapped[str] = mapped_column(Text, default="")


class Plan(TimestampMixin, StatusMixin, Base):
    __tablename__ = "plans"

    plan_type: Mapped[str] = mapped_column(String(40), default="daily")
    period: Mapped[str] = mapped_column(String(40), default="")
    owner: Mapped[str] = mapped_column(String(120), default="")
    target_items: Mapped[str] = mapped_column(Text, default="")
    project_items: Mapped[str] = mapped_column(Text, default="")
    action_items: Mapped[str] = mapped_column(Text, default="")
    support_needed: Mapped[str] = mapped_column(Text, default="")


class DailyReport(TimestampMixin, StatusMixin, Base):
    __tablename__ = "daily_reports"

    report_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    owner: Mapped[str] = mapped_column(String(120), index=True)
    planned_items: Mapped[str] = mapped_column(Text, default="")
    completed_items: Mapped[str] = mapped_column(Text, default="")
    unfinished_reason: Mapped[str] = mapped_column(Text, default="")
    new_visits: Mapped[int] = mapped_column(Integer, default=0)
    new_channels: Mapped[int] = mapped_column(Integer, default=0)
    project_progress: Mapped[str] = mapped_column(Text, default="")
    contract_payment_progress: Mapped[str] = mapped_column(Text, default="")
    tomorrow_plan: Mapped[str] = mapped_column(Text, default="")
    support_needed: Mapped[str] = mapped_column(Text, default="")


class GeneratedReport(TimestampMixin, StatusMixin, Base):
    __tablename__ = "generated_reports"

    report_type: Mapped[str] = mapped_column(String(40), index=True)
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    month: Mapped[str] = mapped_column(String(20), default="")
    owner: Mapped[str] = mapped_column(String(120), default="")
    title: Mapped[str] = mapped_column(String(240), default="")
    content: Mapped[str] = mapped_column(Text, default="")
    ai_enhanced: Mapped[bool] = mapped_column(Boolean, default=False)


class AuditLog(TimestampMixin, Base):
    __tablename__ = "audit_logs"

    entity_type: Mapped[str] = mapped_column(String(80), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    action: Mapped[str] = mapped_column(String(40), index=True)
    actor: Mapped[str] = mapped_column(String(120), default="system")
    summary: Mapped[str] = mapped_column(Text, default="")
