const state = {
  section: "dashboard",
  resource: "opportunities",
  records: [],
  selected: null,
  dashboard: null,
};

const sectionConfig = {
  dashboard: {
    title: "首页驾驶舱",
    subtitle: "未来收入、签约结果、现金回款、交付进度集中查看。",
    resources: ["opportunities", "contracts", "receivables", "delivery-projects"],
  },
  customers: {
    title: "渠道客户",
    subtitle: "维护客户、渠道、拜访动作，并从拜访生成商机。",
    resources: ["customers", "channels", "visits"],
  },
  opportunities: {
    title: "储备项目",
    subtitle: "以储备项目为核心管理项目漏斗和签约预测。",
    resources: ["opportunities", "group-projects"],
  },
  contracts: {
    title: "合同回款",
    subtitle: "合同、应收、回款分开管理，避免签约额重复计算。",
    resources: ["contracts", "receivables", "payments"],
  },
  delivery: {
    title: "项目实施",
    subtitle: "跟踪交付节点、成果文件、客户确认和延期事项。",
    resources: ["delivery-projects"],
  },
  reports: {
    title: "计划汇报",
    subtitle: "日报汇总周报，月计划和台账数据生成月复盘草稿。",
    resources: ["plans", "daily-reports", "generated-reports"],
  },
  settings: {
    title: "系统设置",
    subtitle: "维护人员、字段选项、AI 配置和操作日志。",
    resources: ["users", "settings/options", "audit-logs"],
  },
};

const resources = {
  customers: {
    label: "客户",
    title: "客户基础信息",
    description: "一个客户或合作对象一条记录。",
    endpoint: "/api/customers",
    columns: ["name", "customer_type", "customer_nature", "industry", "region", "owner", "status"],
    fields: ["name", "customer_type", "customer_nature", "industry", "region", "contact_person", "contact_phone", "customer_level", "owner"],
  },
  channels: {
    label: "渠道",
    title: "渠道合伙人台账",
    description: "判断渠道能否持续带来客户、项目、信息或协同机会。",
    endpoint: "/api/channels",
    columns: ["organization", "channel_category", "resource_type", "business_owner", "estimated_amount", "next_action"],
    fields: ["channel_category", "organization", "contact_person", "key_resource", "resource_type", "related_business", "cooperation_stage", "channel_level", "owner", "business_owner", "estimated_amount", "latest_contact_date", "next_action"],
  },
  visits: {
    label: "拜访",
    title: "客户拜访台账",
    description: "记录一次拜访或有效沟通，可转储备项目。",
    endpoint: "/api/visits",
    columns: ["visit_date", "customer_name", "related_project", "business_owner", "result", "next_action"],
    fields: ["visit_date", "customer_name", "visit_target", "visit_purpose", "related_project", "business_detail", "business_owner", "key_notes", "result", "estimated_amount", "next_action", "deadline", "is_opportunity"],
  },
  opportunities: {
    label: "储备项目",
    title: "公司项目汇总",
    description: "管理未来合同来源，支持一键转合同。",
    endpoint: "/api/opportunities",
    columns: ["project_name", "customer_name", "business_segment", "project_stage", "estimated_contract_amount", "business_owner", "is_converted"],
    fields: ["project_name", "customer_name", "customer_level", "customer_category", "customer_nature", "province", "city", "business_segment", "business_detail", "project_source", "project_stage", "estimated_contract_amount", "expected_sign_month", "is_key_project", "business_owner", "latest_follow_date", "follow_status", "remark"],
  },
  "group-projects": {
    label: "集团项目",
    title: "集团融合项目",
    description: "体现北京公司牵引集团和协同兄弟公司的经营定位。",
    endpoint: "/api/group-projects",
    columns: ["brother_company", "project_name", "customer_name", "project_stage", "weighted_amount", "beijing_owner", "next_action"],
    fields: ["brother_company", "project_name", "customer_name", "business_segment", "project_source", "project_stage", "estimated_amount", "success_probability", "weighted_amount", "beijing_owner", "branch_contact", "collaboration_method", "next_action", "planned_completion_date"],
  },
  contracts: {
    label: "合同",
    title: "合同台账",
    description: "一份合同一行，只记录签约事实。",
    endpoint: "/api/contracts",
    columns: ["contract_number", "contract_name", "customer_name", "business_segment", "contract_amount", "business_owner", "payment_method"],
    fields: ["application_date", "contract_return_date", "contract_number", "contract_name", "customer_name", "customer_category", "industry_category", "region", "business_segment", "business_detail", "business_owner", "contract_amount", "tax_rate", "direct_cost", "estimated_gross_profit", "service_period", "contract_due_date", "payment_method", "is_key_project", "is_group_collaboration", "remark"],
  },
  receivables: {
    label: "应收",
    title: "应收款台账",
    description: "记录现金流计划和欠款状态，不反推签约额。",
    endpoint: "/api/receivables",
    columns: ["contract_number", "customer_name", "project_name", "total_outstanding", "planned_payment_month", "collection_status"],
    fields: ["contract_number", "customer_name", "project_name", "contract_amount", "total_outstanding", "collectible_amount", "uncollectible_amount", "invoiced_amount", "payment_condition", "contract_due_date", "overdue_days", "collection_status", "planned_payment_month", "planned_payment_amount", "business_owner"],
  },
  payments: {
    label: "回款",
    title: "回款明细",
    description: "每笔到账追加一行，用于核销应收。",
    endpoint: "/api/payments",
    columns: ["arrival_date", "contract_number", "customer_name", "project_name", "payment_amount", "payment_method"],
    fields: ["arrival_date", "contract_number", "customer_name", "project_name", "payment_amount", "payment_method", "remark"],
  },
  "delivery-projects": {
    label: "实施",
    title: "实施项目进度",
    description: "避免合同签订后交付无人跟、验收无人催、成果无人归档。",
    endpoint: "/api/delivery-projects",
    columns: ["project_name", "contract_number", "customer_name", "delivery_stage", "project_owner", "support_needed"],
    fields: ["project_name", "contract_number", "customer_name", "business_type", "project_owner", "delivery_stage", "planned_start_date", "planned_completion_date", "actual_completion_date", "current_progress", "deliverable_files", "customer_confirmation_status", "delay_reason", "support_needed"],
  },
  plans: {
    label: "计划",
    title: "计划管理",
    description: "月计划、周计划和日计划承接经营目标。",
    endpoint: "/api/plans",
    columns: ["plan_type", "period", "owner", "target_items", "support_needed"],
    fields: ["plan_type", "period", "owner", "target_items", "project_items", "action_items", "support_needed"],
  },
  "daily-reports": {
    label: "日报",
    title: "日报",
    description: "日计划带入日报，补充完成结果和需协调事项。",
    endpoint: "/api/daily-reports",
    columns: ["report_date", "owner", "completed_items", "project_progress", "support_needed"],
    fields: ["report_date", "owner", "planned_items", "completed_items", "unfinished_reason", "new_visits", "new_channels", "project_progress", "contract_payment_progress", "tomorrow_plan", "support_needed"],
  },
  "generated-reports": {
    label: "汇报草稿",
    title: "已生成草稿",
    description: "周报和月复盘草稿记录。",
    endpoint: "/api/generated-reports",
    columns: ["report_type", "title", "owner", "month", "ai_enhanced", "created_at"],
    fields: ["report_type", "owner", "title", "content"],
  },
  users: {
    label: "人员",
    title: "人员角色",
    description: "简化用户和角色维护。",
    endpoint: "/api/users",
    columns: ["name", "role", "username", "status"],
    fields: ["name", "role", "username", "status"],
  },
  "settings/options": {
    label: "字段选项",
    title: "字段字典",
    description: "统一项目阶段、业务板块、客户类型等口径。",
    endpoint: "/api/settings/options",
    columns: ["category", "value", "sort_order", "status"],
    fields: ["category", "value", "sort_order", "status"],
  },
  "audit-logs": {
    label: "操作日志",
    title: "操作日志",
    description: "关键数据新增、修改、作废和自动生成记录。",
    endpoint: "/api/audit-logs",
    columns: ["entity_type", "entity_id", "action", "actor", "summary", "created_at"],
    fields: [],
    readonly: true,
  },
};

const labels = {
  name: "名称",
  customer_type: "客户大类",
  customer_nature: "客户性质",
  industry: "行业",
  region: "区域",
  contact_person: "联系人",
  contact_phone: "联系方式",
  customer_level: "客户等级",
  customer_category: "客户大类",
  owner: "负责人",
  status: "状态",
  channel_category: "渠道类别",
  organization: "所属单位",
  key_resource: "关键资源",
  resource_type: "资源类型",
  related_business: "关联业务",
  cooperation_stage: "合作阶段",
  channel_level: "渠道等级",
  business_owner: "商务负责人",
  lead_count: "线索数",
  opportunity_count: "商机数",
  estimated_amount: "预计金额",
  latest_contact_date: "最近沟通",
  next_action: "下一步动作",
  visit_date: "拜访日期",
  customer_name: "客户名称",
  visit_target: "拜访对象",
  visit_purpose: "拜访目的",
  related_project: "关联项目",
  business_detail: "业务细分",
  key_notes: "关键纪要",
  result: "形成成果",
  deadline: "完成期限",
  is_opportunity: "形成商机",
  project_name: "项目名称",
  brother_company: "兄弟公司",
  province: "省份",
  city: "城市",
  business_segment: "业务板块",
  project_source: "项目来源",
  project_stage: "项目阶段",
  estimated_contract_amount: "预计合同金额",
  expected_sign_month: "预计签约月份",
  is_key_project: "重点项目",
  is_converted: "已转合同",
  follow_status: "跟进状态",
  latest_follow_date: "最新跟进",
  remark: "备注",
  success_probability: "成功概率",
  weighted_amount: "加权金额",
  beijing_owner: "北京负责人",
  branch_contact: "分公司对接人",
  collaboration_method: "协同方式",
  planned_completion_date: "计划完成",
  contract_number: "合同编号",
  contract_name: "合同名称",
  application_date: "申请日期",
  contract_return_date: "合同回归",
  industry_category: "行业类别",
  collaboration_unit: "协同单位",
  contract_amount: "合同金额",
  tax_rate: "税率",
  direct_cost: "直接成本",
  estimated_gross_profit: "预计毛利",
  service_period: "服务周期",
  contract_due_date: "合同到期",
  payment_method: "付款方式",
  is_group_collaboration: "集团协同",
  total_outstanding: "未收金额",
  collectible_amount: "具备回款",
  uncollectible_amount: "不具备回款",
  invoiced_amount: "已开发票",
  payment_condition: "付款条件",
  overdue_days: "逾期天数",
  collection_status: "催收状态",
  planned_payment_month: "计划回款月份",
  planned_payment_amount: "计划回款金额",
  arrival_date: "到账日期",
  payment_amount: "收款金额",
  delivery_stage: "实施阶段",
  business_type: "业务类型",
  project_owner: "项目负责人",
  planned_start_date: "计划开始",
  actual_completion_date: "实际完成",
  current_progress: "当前进度",
  deliverable_files: "成果文件",
  customer_confirmation_status: "客户确认",
  delay_reason: "延期说明",
  support_needed: "需协调事项",
  plan_type: "计划类型",
  period: "周期",
  target_items: "目标事项",
  project_items: "项目事项",
  action_items: "动作事项",
  report_date: "日报日期",
  planned_items: "计划事项",
  completed_items: "完成事项",
  unfinished_reason: "未完成原因",
  new_visits: "新增拜访",
  new_channels: "新增渠道",
  project_progress: "项目推进",
  contract_payment_progress: "合同回款进展",
  tomorrow_plan: "明日计划",
  report_type: "汇报类型",
  title: "标题",
  month: "月份",
  ai_enhanced: "AI增强",
  content: "内容",
  entity_type: "对象类型",
  entity_id: "对象ID",
  action: "动作",
  actor: "操作人",
  summary: "摘要",
  created_at: "创建时间",
  sort_order: "排序",
  username: "登录名",
  role: "角色",
};

document.addEventListener("DOMContentLoaded", () => {
  bindEvents();
  switchSection("dashboard");
});

function bindEvents() {
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => switchSection(button.dataset.section));
  });
  document.getElementById("refresh-btn").addEventListener("click", refreshAll);
  document.getElementById("new-record-btn").addEventListener("click", () => document.querySelector("#record-form input, #record-form textarea, #record-form select")?.focus());
  document.getElementById("search-box").addEventListener("input", renderTable);
  document.getElementById("convert-btn").addEventListener("click", runConversion);
  document.getElementById("weekly-btn").addEventListener("click", generateWeeklyReport);
  document.getElementById("monthly-btn").addEventListener("click", generateMonthlyReport);
  document.getElementById("record-form").addEventListener("submit", submitRecord);
}

async function switchSection(section) {
  state.section = section;
  const config = sectionConfig[section];
  state.resource = config.resources[0];
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.section === section);
  });
  document.getElementById("view-title").textContent = config.title;
  document.getElementById("view-subtitle").textContent = config.subtitle;
  renderResourceTabs();
  await refreshAll();
}

function renderResourceTabs() {
  const holder = document.getElementById("resource-tabs");
  holder.innerHTML = "";
  sectionConfig[state.section].resources.forEach((resourceName) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `segment ${resourceName === state.resource ? "active" : ""}`;
    button.textContent = resources[resourceName].label;
    button.addEventListener("click", async () => {
      state.resource = resourceName;
      state.selected = null;
      renderResourceTabs();
      await refreshRecords();
    });
    holder.appendChild(button);
  });
}

async function refreshAll() {
  await Promise.all([refreshDashboard(), refreshRecords()]);
}

async function refreshDashboard() {
  const summary = await api("/api/dashboard/summary");
  state.dashboard = summary;
  document.getElementById("metric-contract").textContent = formatMoney(summary.total_contract_amount);
  document.getElementById("metric-payment").textContent = formatMoney(summary.total_payment_amount);
  document.getElementById("metric-pipeline").textContent = formatMoney(summary.pipeline_estimated_amount);
  document.getElementById("metric-receivable").textContent = formatMoney(summary.receivable_outstanding);
  renderFunnel(summary);
  renderAlerts(summary);
}

async function refreshRecords() {
  const config = resources[state.resource];
  document.getElementById("ledger-title").textContent = config.title;
  document.getElementById("ledger-description").textContent = config.description;
  document.getElementById("form-title").textContent = `${config.label}快速录入`;
  document.getElementById("form-hint").textContent = config.readonly ? "该视图只读。" : "保存后自动写入台账并留下操作记录。";
  document.getElementById("convert-btn").style.display = state.resource === "opportunities" || state.resource === "visits" || state.resource === "contracts" ? "inline-block" : "none";
  state.records = await api(config.endpoint);
  renderTable();
  renderForm();
}

function renderFunnel(summary) {
  const rows = [
    ["储备金额", summary.pipeline_estimated_amount],
    ["签约金额", summary.total_contract_amount],
    ["回款金额", summary.total_payment_amount],
  ];
  const max = Math.max(...rows.map((item) => Number(item[1]) || 0), 1);
  document.getElementById("funnel-bars").innerHTML = rows
    .map(([label, value]) => {
      const width = Math.max(6, Math.round((Number(value) / max) * 100));
      return `<div class="funnel-row"><span>${label}</span><div class="bar"><span style="width:${width}%"></span></div><strong>${formatMoney(value)}</strong></div>`;
    })
    .join("");
}

function renderAlerts(summary) {
  document.getElementById("receivable-alerts").innerHTML = `
    <li>应收未收：${formatMoney(summary.receivable_outstanding)}</li>
    <li>延期实施项目：${summary.delayed_delivery_count} 个</li>
    <li>重点推进项目：${summary.key_project_count} 个</li>
  `;
  document.getElementById("todo-list").innerHTML = `
    <li>本周优先更新重点项目下一步动作。</li>
    <li>合同确认后及时初始化应收和实施进度。</li>
    <li>日报中的需协调事项将进入周报草稿。</li>
  `;
}

function renderTable() {
  const config = resources[state.resource];
  const filter = document.getElementById("search-box").value.trim().toLowerCase();
  const records = state.records.filter((record) => JSON.stringify(record).toLowerCase().includes(filter));
  document.getElementById("ledger-head").innerHTML = `<tr>${config.columns.map((key) => `<th>${labels[key] || key}</th>`).join("")}</tr>`;
  if (records.length === 0) {
    document.getElementById("ledger-body").innerHTML = `<tr><td class="empty-cell" colspan="${config.columns.length}">暂无数据，使用右侧表单新增记录。</td></tr>`;
    return;
  }
  document.getElementById("ledger-body").innerHTML = records
    .map((record) => {
      const selected = state.selected && state.selected.id === record.id ? "selected" : "";
      const cells = config.columns.map((key) => `<td>${formatValue(record[key])}</td>`).join("");
      return `<tr class="${selected}" data-id="${record.id}">${cells}</tr>`;
    })
    .join("");
  document.querySelectorAll("#ledger-body tr[data-id]").forEach((row) => {
    row.addEventListener("click", () => {
      state.selected = state.records.find((record) => String(record.id) === row.dataset.id);
      renderTable();
    });
  });
}

function renderForm() {
  const config = resources[state.resource];
  const form = document.getElementById("record-form");
  if (config.readonly) {
    form.innerHTML = `<p class="muted">该视图用于查看系统记录，不支持直接新增。</p>`;
    return;
  }
  form.innerHTML = config.fields
    .map((field) => {
      const label = labels[field] || field;
      if (field.includes("remark") || field.includes("items") || field.includes("progress") || field.includes("support") || field.includes("content") || field.includes("notes") || field.includes("action")) {
        return `<label class="field"><span>${label}</span><textarea name="${field}" rows="3"></textarea></label>`;
      }
      if (field.startsWith("is_") || field.endsWith("_initialized")) {
        return `<label class="field"><span>${label}</span><select name="${field}"><option value="false">否</option><option value="true">是</option></select></label>`;
      }
      return `<label class="field"><span>${label}</span><input name="${field}" type="${inputType(field)}"></label>`;
    })
    .join("") + `<div class="form-actions"><button class="primary-btn" type="submit">保存记录</button><button class="secondary-btn" type="reset">清空</button></div>`;
}

async function submitRecord(event) {
  event.preventDefault();
  const config = resources[state.resource];
  if (config.readonly) return;
  const formData = new FormData(event.target);
  const payload = {};
  for (const [key, value] of formData.entries()) {
    if (value === "") continue;
    if (value === "true" || value === "false") {
      payload[key] = value === "true";
    } else if (key.includes("amount") || key.includes("cost") || key.includes("rate") || key.includes("count") || key.includes("days") || key.includes("probability")) {
      payload[key] = Number(value);
    } else {
      payload[key] = value;
    }
  }
  await api(config.endpoint, { method: "POST", body: JSON.stringify(payload) });
  event.target.reset();
  await refreshAll();
}

async function runConversion() {
  if (!state.selected) {
    alert("请先在表格中选择一条记录。");
    return;
  }
  let endpoint = "";
  if (state.resource === "visits") endpoint = `/api/visits/${state.selected.id}/convert-to-opportunity`;
  if (state.resource === "opportunities") endpoint = `/api/opportunities/${state.selected.id}/convert-to-contract`;
  if (state.resource === "contracts") endpoint = `/api/contracts/${state.selected.id}/initialize-receivable-and-delivery`;
  if (!endpoint) return;
  await api(endpoint, { method: "POST" });
  await refreshAll();
}

async function generateWeeklyReport() {
  const payload = {
    period_start: startOfWeek(),
    period_end: today(),
    owner: document.getElementById("owner-filter").value,
  };
  const report = await api("/api/reports/weekly/draft", { method: "POST", body: JSON.stringify(payload) });
  document.getElementById("report-output").textContent = report.content;
}

async function generateMonthlyReport() {
  const now = new Date();
  const payload = {
    month: `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`,
    owner: document.getElementById("owner-filter").value,
  };
  const report = await api("/api/reports/monthly-review/draft", { method: "POST", body: JSON.stringify(payload) });
  document.getElementById("report-output").textContent = report.content;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`${path} failed: ${response.status}`);
  }
  return response.json();
}

function inputType(field) {
  if (field.includes("date")) return "date";
  if (field.includes("amount") || field.includes("cost") || field.includes("rate") || field.includes("count") || field.includes("days") || field.includes("probability")) return "number";
  return "text";
}

function formatMoney(value) {
  const number = Number(value || 0);
  if (number >= 10000) return `${(number / 10000).toFixed(1)}万`;
  return number.toFixed(0);
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "boolean") return value ? "是" : "否";
  if (typeof value === "number") return value.toLocaleString("zh-CN");
  return String(value);
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function startOfWeek() {
  const date = new Date();
  const day = date.getDay() || 7;
  date.setDate(date.getDate() - day + 1);
  return date.toISOString().slice(0, 10);
}
