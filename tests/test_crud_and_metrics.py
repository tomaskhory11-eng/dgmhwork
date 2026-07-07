def test_customer_create_list_update_archive(client):
    created = client.post(
        "/api/customers",
        json={
            "name": "北京示例科技有限公司",
            "customer_type": "政府平台",
            "customer_nature": "国企",
            "industry": "生态环境",
            "region": "北京",
            "contact_person": "王主任",
            "contact_phone": "010-00000000",
            "customer_level": "A",
            "owner": "张旭",
            "status": "有效",
        },
    )
    assert created.status_code == 200
    customer_id = created.json()["id"]

    listed = client.get("/api/customers")
    assert listed.status_code == 200
    assert any(item["id"] == customer_id for item in listed.json())

    updated = client.patch(f"/api/customers/{customer_id}", json={"customer_level": "B"})
    assert updated.status_code == 200
    assert updated.json()["customer_level"] == "B"

    archived = client.patch(f"/api/customers/{customer_id}", json={"status": "作废"})
    assert archived.status_code == 200
    assert archived.json()["status"] == "作废"


def test_audit_log_records_create_and_update(client):
    created = client.post(
        "/api/channels",
        json={
            "channel_category": "设计院/咨询机构",
            "organization": "示例设计院",
            "contact_person": "李工",
            "key_resource": "园区项目线索",
            "resource_type": "项目线索",
            "related_business": "环评/验收/排污许可",
            "cooperation_stage": "接触中",
            "channel_level": "B",
            "owner": "李绪志",
            "business_owner": "李绪志",
            "lead_count": 1,
            "opportunity_count": 0,
            "estimated_amount": 300000,
            "latest_contact_date": "2026-07-07",
            "next_action": "约二次沟通",
        },
    )
    assert created.status_code == 200

    logs = client.get("/api/audit-logs")
    assert logs.status_code == 200
    assert any(log["entity_type"] == "channels" and log["action"] == "create" for log in logs.json())
