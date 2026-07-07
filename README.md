# 北京公司经营管理 AI Agent

本工程是北京公司办公自动化经营管理系统的本地网页应用和后端原型。它以经营过程管理为核心，连接客户、渠道、拜访、储备项目、合同、应收、回款、实施进度、计划汇报和经营看板。

## 本地启动

```powershell
cd D:\degu-oa-agent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\start-local.ps1
```

打开：

```text
http://127.0.0.1:8766/
```

## 当前能力

- 首页驾驶舱：签约额、回款额、储备项目额、应收未收、重点事项。
- 台账管理：客户、渠道、拜访、储备项目、集团项目、合同、应收、回款、实施、计划、日报。
- 业务转化：拜访转储备项目、储备项目转合同、合同初始化应收和实施进度。
- 自动汇报：周报草稿、月复盘草稿。
- 系统配置：人员、字段选项、AI 配置占位、操作日志。

## 测试

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## 云部署预留

后端是 FastAPI，数据库连接从 `DATABASE_URL` 读取。早期本地使用 SQLite，正式多人云端使用前建议迁移 PostgreSQL。

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/degu_oa
uvicorn app.main:app --host 0.0.0.0 --port 8766
```

推荐云端形态：

```text
Nginx -> Uvicorn/FastAPI -> PostgreSQL
```

## 说明

未配置 AI API 时，系统仍使用本地规则生成周报和月复盘草稿。后续接入 OpenAI-compatible 或 DeepSeek 模型时，模型输出只作为草稿增强，不直接修改关键台账字段。
