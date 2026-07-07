from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FieldOption, User


DEFAULT_OPTIONS = [
    ("project_stage", "线索"),
    ("project_stage", "有效商机"),
    ("project_stage", "需求沟通"),
    ("project_stage", "方案编制"),
    ("project_stage", "报价"),
    ("project_stage", "商务谈判"),
    ("project_stage", "待签约"),
    ("project_stage", "已签约"),
    ("business_segment", "中央生态环保督察整改"),
    ("business_segment", "中央环保资金申请"),
    ("business_segment", "高端环保咨询"),
    ("business_segment", "环评/验收/排污许可"),
    ("business_segment", "环境应急预案"),
    ("customer_category", "政府平台"),
    ("customer_category", "工业企业"),
    ("customer_category", "园区"),
    ("customer_nature", "国企"),
    ("customer_nature", "民企"),
    ("customer_nature", "政府机关"),
    ("payment_method", "一次性付款"),
    ("payment_method", "分期付款"),
]

DEFAULT_USERS = [
    ("总经理", "总经理", "manager"),
    ("综合管理岗", "综合管理岗", "admin-office"),
    ("李绪志", "商务人员", "lixuzhi"),
    ("张旭", "商务人员", "zhangxu"),
    ("袁浩洋", "商务人员", "yuanhaoyang"),
    ("技术负责人", "技术/实施人员", "delivery"),
]


def seed_defaults(session: Session) -> None:
    has_options = session.scalar(select(FieldOption.id).limit(1))
    if not has_options:
        for order, (category, value) in enumerate(DEFAULT_OPTIONS, start=1):
            session.add(FieldOption(category=category, value=value, sort_order=order))

    has_users = session.scalar(select(User.id).limit(1))
    if not has_users:
        for name, role, username in DEFAULT_USERS:
            session.add(User(name=name, role=role, username=username))

    session.commit()
