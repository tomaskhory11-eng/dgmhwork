# Degu OA Agent MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first runnable local web app and backend prototype for the Beijing company operating-management AI Agent.

**Architecture:** A FastAPI application serves both JSON APIs and a code-native static web workstation. SQLite stores operational ledgers, workflow links, generated report drafts, settings, users, roles, and audit logs. Local rule-based report generation works without an AI key, while OpenAI-compatible model settings are stored for later enhancement.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2, Pydantic, SQLite, pytest, httpx TestClient, vanilla HTML/CSS/JavaScript, Uvicorn.

## Global Constraints

- The project root is `D:\degu-oa-agent`.
- The app must run locally from Windows with a one-click script and be easy to migrate to a cloud server.
- First-version database is SQLite; design must allow later PostgreSQL migration through a single database URL setting.
- The first screen is the actual workbench, not a landing page.
- The UI must be restrained, dense, business-focused, and optimized for scanning table data.
- No independent risk-control module in MVP.
- The core ledgers are customers, channels, visits, opportunities, group projects, contracts, receivables, payments, delivery projects, plans, daily reports, generated reports, field options, users, and audit logs.
- The three required workflow conversions are visit to opportunity, opportunity to contract, and contract to receivable plus delivery project.
- Weekly and monthly reports are generated as drafts; they do not directly become final management judgment.
- The system must run without an AI API key.
- Model output, when later enabled, must not directly modify key ledger fields.

---

## File Structure

- `requirements.txt`: Python dependency list for local and cloud use.
- `.gitignore`: ignores generated databases, caches, worktrees, local settings, and QA screenshots.
- `README.md`: local start, test, and cloud deployment notes.
- `start-local.ps1` and `start-local.bat`: Windows launchers.
- `app/__init__.py`: application package marker.
- `app/config.py`: settings loaded from environment and optional local JSON.
- `app/database.py`: SQLAlchemy engine/session creation, schema initialization helper.
- `app/models.py`: database table definitions and relationships.
- `app/schemas.py`: request/response schemas.
- `app/seed.py`: default users, options, and demo operational data.
- `app/crud.py`: reusable create/list/update/archive helpers.
- `app/services/audit_log.py`: audit log writer.
- `app/services/metrics.py`: dashboard aggregate metrics.
- `app/services/workflow.py`: conversion workflows.
- `app/services/report_generator.py`: weekly/monthly draft generation.
- `app/services/ai_client.py`: OpenAI-compatible configuration placeholder with safe no-key fallback.
- `app/routers/*.py`: focused API routers.
- `app/main.py`: FastAPI app factory, static file serving, router registration.
- `static/index.html`: code-native workbench shell.
- `static/styles.css`: visual system and responsive layout.
- `static/app.js`: UI state, API client, rendering, forms, conversion actions, report generation.
- `tests/conftest.py`: isolated in-memory database test app.
- `tests/test_health_and_seed.py`: health and seed verification.
- `tests/test_crud_and_metrics.py`: ledger CRUD and dashboard metrics.
- `tests/test_workflows.py`: conversion workflow tests.
- `tests/test_reports.py`: report-generation tests.

### Task 1: Project Skeleton, Settings, and App Factory

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `app/__init__.py`
- Create: `app/config.py`
- Create: `app/database.py`
- Create: `app/main.py`
- Create: `tests/conftest.py`
- Create: `tests/test_health_and_seed.py`

**Interfaces:**
- Produces: `app.main.create_app(database_url: str | None = None) -> FastAPI`
- Produces: `app.database.init_db(engine: Engine) -> None`
- Produces: `app.config.Settings`
- Consumes: no prior application code.

- [ ] **Step 1: Write failing health and seed tests**

Create `tests/conftest.py`:

```python
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    app = create_app("sqlite+pysqlite:///:memory:")
    with TestClient(app) as test_client:
        yield test_client
```

Create `tests/test_health_and_seed.py`:

```python
def test_health_returns_ok(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_seeded_options_are_available(client):
    response = client.get("/api/settings/options")

    assert response.status_code == 200
    payload = response.json()
    option_names = {(item["category"], item["value"]) for item in payload}
    assert ("project_stage", "需求沟通") in option_names
    assert ("business_segment", "中央环保资金申请") in option_names
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_health_and_seed.py -v`

Expected: FAIL because `app.main` or `create_app` does not exist.

- [ ] **Step 3: Write minimal skeleton implementation**

Create `requirements.txt`:

```text
fastapi==0.115.6
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
pydantic==2.10.4
python-multipart==0.0.20
pytest==8.3.4
httpx==0.28.1
```

Create `.gitignore`:

```gitignore
__pycache__/
.pytest_cache/
.venv/
data/*.sqlite3
data/local_settings.json
.worktrees/
tmp/
*.log
```

Create `app/__init__.py`:

```python
"""Beijing company operating-management AI Agent."""
```

Create `app/config.py`, `app/database.py`, and `app/main.py` with enough code for `GET /api/health` and `GET /api/settings/options`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_health_and_seed.py -v`

Expected: PASS with both tests green.

- [ ] **Step 5: Commit**

Run:

```powershell
git add .gitignore requirements.txt app tests
git commit -m "feat: add FastAPI skeleton"
```

### Task 2: Database Models, Seed Data, and Generic CRUD

**Files:**
- Create: `app/models.py`
- Create: `app/schemas.py`
- Create: `app/seed.py`
- Create: `app/crud.py`
- Create: `app/services/audit_log.py`
- Modify: `app/database.py`
- Modify: `app/main.py`
- Create: `tests/test_crud_and_metrics.py`

**Interfaces:**
- Consumes: `create_app(database_url)`
- Produces: SQLAlchemy models for all MVP ledgers.
- Produces: CRUD endpoints for customers, channels, visits, opportunities, group projects, contracts, receivables, payments, delivery projects, plans, daily reports, users, and field options.
- Produces: soft archive via `PATCH /api/{resource}/{id}` with `{"status": "作废"}`.

- [ ] **Step 1: Write failing CRUD test**

Create `tests/test_crud_and_metrics.py`:

```python
def test_customer_create_list_update_archive(client):
    created = client.post("/api/customers", json={
        "name": "北京示例科技有限公司",
        "customer_type": "政府平台",
        "customer_nature": "国企",
        "industry": "生态环境",
        "region": "北京",
        "contact_person": "王主任",
        "contact_phone": "010-00000000",
        "customer_level": "A",
        "owner": "张旭",
        "status": "有效"
    })
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
    created = client.post("/api/channels", json={
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
        "next_action": "约二次沟通"
    })
    assert created.status_code == 200

    logs = client.get("/api/audit-logs")
    assert logs.status_code == 200
    assert any(log["entity_type"] == "channels" and log["action"] == "create" for log in logs.json())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_crud_and_metrics.py -v`

Expected: FAIL because resource routers and models do not exist.

- [ ] **Step 3: Implement models, schemas, seed data, CRUD, and audit logging**

Implement the database tables listed in the design spec. Keep text fields permissive in MVP. Use `Numeric(14, 2)` for money values and ISO date strings in API payloads converted to `date` columns where practical.

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_health_and_seed.py tests/test_crud_and_metrics.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```powershell
git add app tests
git commit -m "feat: add operating ledger models and CRUD"
```

### Task 3: Dashboard Metrics and Workflow Conversions

**Files:**
- Create: `app/services/metrics.py`
- Create: `app/services/workflow.py`
- Create: `app/routers/dashboard.py`
- Modify: `app/main.py`
- Modify: resource routers as needed.
- Create: `tests/test_workflows.py`
- Modify: `tests/test_crud_and_metrics.py`

**Interfaces:**
- Consumes: ledger models from Task 2.
- Produces: `GET /api/dashboard/summary`.
- Produces: `POST /api/visits/{id}/convert-to-opportunity`.
- Produces: `POST /api/opportunities/{id}/convert-to-contract`.
- Produces: `POST /api/contracts/{id}/initialize-receivable-and-delivery`.

- [ ] **Step 1: Write failing workflow and metric tests**

Create `tests/test_workflows.py`:

```python
def test_visit_converts_to_opportunity(client):
    visit = client.post("/api/visits", json={
        "visit_date": "2026-07-07",
        "customer_name": "北京示例科技有限公司",
        "visit_target": "环保负责人",
        "contact_info": "010-00000000",
        "visit_purpose": "中央环保资金项目沟通",
        "related_project": "绿色低碳改造项目",
        "business_detail": "中央环保资金申请",
        "business_owner": "张旭",
        "participants": "张旭",
        "key_notes": "客户有申报需求",
        "customer_attitude": "积极",
        "result": "形成商机",
        "estimated_amount": 800000,
        "next_action": "提交申报条件清单",
        "deadline": "2026-07-14",
        "is_opportunity": True
    }).json()

    converted = client.post(f"/api/visits/{visit['id']}/convert-to-opportunity")

    assert converted.status_code == 200
    payload = converted.json()
    assert payload["project_name"] == "绿色低碳改造项目"
    assert payload["customer_name"] == "北京示例科技有限公司"
    assert payload["estimated_contract_amount"] == 800000


def test_opportunity_converts_to_contract_then_initializes_receivable_and_delivery(client):
    opportunity = client.post("/api/opportunities", json={
        "project_name": "绿色低碳改造项目",
        "customer_name": "北京示例科技有限公司",
        "customer_level": "A",
        "customer_category": "工业企业",
        "customer_nature": "民企",
        "province": "北京",
        "city": "北京",
        "business_segment": "中央环保资金申请",
        "business_detail": "资金申报",
        "project_source": "客户拜访",
        "project_stage": "商务谈判",
        "estimated_contract_amount": 800000,
        "expected_sign_month": "2026-08",
        "is_key_project": True,
        "business_owner": "张旭",
        "latest_follow_date": "2026-07-07",
        "follow_status": "推进中",
        "is_converted": False,
        "remark": "重点推进"
    }).json()

    contract = client.post(f"/api/opportunities/{opportunity['id']}/convert-to-contract").json()
    assert contract["contract_name"] == "绿色低碳改造项目"
    assert contract["contract_amount"] == 800000

    initialized = client.post(f"/api/contracts/{contract['id']}/initialize-receivable-and-delivery")
    assert initialized.status_code == 200
    payload = initialized.json()
    assert payload["receivable"]["project_name"] == "绿色低碳改造项目"
    assert payload["delivery_project"]["project_name"] == "绿色低碳改造项目"
```

Append to `tests/test_crud_and_metrics.py`:

```python
def test_dashboard_summary_reflects_contract_payment_and_pipeline(client):
    client.post("/api/contracts", json={
        "application_date": "2026-07-01",
        "contract_return_date": "2026-07-06",
        "contract_number": "DG-BJ-2026-001",
        "contract_name": "示例环评项目",
        "customer_name": "北京示例科技有限公司",
        "customer_category": "工业企业",
        "industry_category": "生态环境",
        "region": "北京",
        "business_segment": "环评/验收/排污许可",
        "business_detail": "环评",
        "business_owner": "李绪志",
        "collaboration_unit": "",
        "contract_amount": 500000,
        "tax_rate": 0.06,
        "direct_cost": 180000,
        "estimated_gross_profit": 290000,
        "service_period": "2026-07 至 2026-12",
        "contract_due_date": "2026-12-31",
        "payment_method": "分期付款",
        "is_key_project": True,
        "is_group_collaboration": False,
        "remark": ""
    })
    client.post("/api/payments", json={
        "arrival_date": "2026-07-07",
        "contract_number": "DG-BJ-2026-001",
        "customer_name": "北京示例科技有限公司",
        "project_name": "示例环评项目",
        "payment_amount": 120000,
        "payment_method": "银行转账",
        "remark": ""
    })

    summary = client.get("/api/dashboard/summary")

    assert summary.status_code == 200
    payload = summary.json()
    assert payload["total_contract_amount"] >= 500000
    assert payload["total_payment_amount"] >= 120000
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_workflows.py tests/test_crud_and_metrics.py -v`

Expected: FAIL because workflow and dashboard endpoints are missing.

- [ ] **Step 3: Implement metrics and workflow services**

Implement workflow functions with duplicate guards and audit log entries. Implement dashboard metrics using SQL aggregate queries and simple Python totals.

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_health_and_seed.py tests/test_crud_and_metrics.py tests/test_workflows.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```powershell
git add app tests
git commit -m "feat: add dashboard metrics and workflow conversions"
```

### Task 4: Report Draft Generation and AI Settings Placeholder

**Files:**
- Create: `app/services/report_generator.py`
- Create: `app/services/ai_client.py`
- Create: `app/routers/reports.py`
- Modify: `app/main.py`
- Create: `tests/test_reports.py`

**Interfaces:**
- Consumes: plans, daily reports, visits, opportunities, contracts, payments, delivery projects.
- Produces: `POST /api/reports/weekly/draft`.
- Produces: `POST /api/reports/monthly-review/draft`.
- Produces: `GET/POST/PATCH /api/settings/ai`.

- [ ] **Step 1: Write failing report tests**

Create `tests/test_reports.py`:

```python
def test_weekly_report_draft_uses_daily_report_and_ledgers(client):
    client.post("/api/daily-reports", json={
        "report_date": "2026-07-07",
        "owner": "张旭",
        "planned_items": "拜访北京示例科技有限公司",
        "completed_items": "完成客户拜访并形成资金申报商机",
        "unfinished_reason": "",
        "new_visits": 1,
        "new_channels": 0,
        "project_progress": "绿色低碳改造项目进入需求沟通",
        "contract_payment_progress": "待确认付款节点",
        "tomorrow_plan": "提交资料清单",
        "support_needed": "需技术确认申报条件"
    })

    response = client.post("/api/reports/weekly/draft", json={
        "period_start": "2026-07-06",
        "period_end": "2026-07-12",
        "owner": "张旭"
    })

    assert response.status_code == 200
    payload = response.json()
    assert payload["report_type"] == "weekly"
    assert "完成客户拜访" in payload["content"]
    assert "需技术确认申报条件" in payload["content"]


def test_monthly_review_draft_works_without_ai_key(client):
    response = client.post("/api/reports/monthly-review/draft", json={
        "month": "2026-07",
        "owner": "公司"
    })

    assert response.status_code == 200
    payload = response.json()
    assert payload["report_type"] == "monthly_review"
    assert "目标完成情况" in payload["content"]
    assert payload["ai_enhanced"] is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_reports.py -v`

Expected: FAIL because report endpoints are missing.

- [ ] **Step 3: Implement report generator and AI settings fallback**

Generate structured Chinese Markdown drafts from local data. Store the generated draft in `generated_reports`. Save AI settings without requiring a key; return `ai_enhanced: false` when no key is configured.

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/test_reports.py tests/test_workflows.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```powershell
git add app tests
git commit -m "feat: add report draft generation"
```

### Task 5: Workbench UI Concept, Static Frontend, and Local Launchers

**Files:**
- Create: `static/index.html`
- Create: `static/styles.css`
- Create: `static/app.js`
- Modify: `app/main.py`
- Create: `start-local.ps1`
- Create: `start-local.bat`
- Create: `README.md`

**Interfaces:**
- Consumes: all API routes from Tasks 1-4.
- Produces: browser workbench at `http://127.0.0.1:8766/`.
- Produces: local launch scripts.

- [ ] **Step 1: Generate the visual concept**

Use Image Gen for a single dense dashboard/workbench concept. Prompt:

```text
Use case: ui-mockup
Asset type: full primary screen concept for a local business operations management web app
Primary request: A restrained Chinese enterprise operating-management AI Agent dashboard for 北京德谷明海环境技术有限公司. The first screen is the usable workbench, not a marketing page.
Layout: left sidebar navigation, compact top bar, KPI strip, project funnel and receivable alert panels, dense ledger table, right-side report draft/action panel.
Visible navigation text: 首页驾驶舱, 渠道客户, 储备项目, 合同回款, 项目实施, 计划汇报, 系统设置.
Visible controls: 新增记录, 转合同, 生成周报, 生成月复盘.
Style/medium: polished product UI mockup, code-native text, enterprise dashboard, restrained and utilitarian.
Color palette: true white background, charcoal text, light gray borders, restrained teal and amber accents, no purple gradient, no decorative blobs.
Constraints: no landing-page hero, no marketing copy, no nested cards, no oversized type, no stock photos, no illegible tiny text, no fake unrelated metrics.
```

Save the accepted concept under `docs/design/oa-agent-workbench-concept.png`.

- [ ] **Step 2: Write failing frontend smoke test**

Append to `tests/test_health_and_seed.py`:

```python
def test_static_workbench_served(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "北京公司经营管理 AI Agent" in response.text
    assert "首页驾驶舱" in response.text
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python -m pytest tests/test_health_and_seed.py::test_static_workbench_served -v`

Expected: FAIL because static workbench is not served.

- [ ] **Step 4: Implement static workbench**

Implement the dashboard in code-native HTML/CSS/JS using the concept as visual reference. Include working navigation tabs, ledger table rendering, modal-like form area, workflow buttons, report draft output, and responsive collapse for narrower screens.

- [ ] **Step 5: Run tests**

Run: `python -m pytest tests/test_health_and_seed.py tests/test_reports.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

Run:

```powershell
git add static app/main.py start-local.ps1 start-local.bat README.md tests docs/design
git commit -m "feat: add local web workbench"
```

### Task 6: End-to-End Verification and Cloud-Ready Documentation

**Files:**
- Modify: `README.md`
- Modify: `app/config.py` if cloud deployment notes reveal missing env settings.
- Modify: `.gitignore` if generated QA files appear.

**Interfaces:**
- Consumes: complete app from Tasks 1-5.
- Produces: verified local server URL.
- Produces: README commands for local Windows and cloud Linux deployment.

- [ ] **Step 1: Run full automated test suite**

Run: `python -m pytest -v`

Expected: all tests PASS.

- [ ] **Step 2: Start local server**

Run: `.\start-local.ps1`

Expected: Uvicorn starts on `http://127.0.0.1:8766/`.

- [ ] **Step 3: Verify rendered frontend**

Use Browser plugin if available. If absent, use Playwright. Validate the flow: app loads -> first meaningful dashboard renders -> switching ledger tabs works -> generating a weekly draft updates the report panel.

- [ ] **Step 4: Verify API workflow manually**

Run API calls or use the UI to create a visit, convert it to an opportunity, convert an opportunity to a contract, initialize receivable and delivery, and generate a monthly review draft.

- [ ] **Step 5: Update README with exact commands**

Include:

```powershell
cd D:\degu-oa-agent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\start-local.ps1
```

Include cloud sketch:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/degu_oa
uvicorn app.main:app --host 0.0.0.0 --port 8766
```

- [ ] **Step 6: Commit**

Run:

```powershell
git add README.md app .gitignore
git commit -m "docs: add verification and deployment notes"
```
