const DEMO_EVIDENCE = [
  { name: "Information_Security_Policy.pdf", type: "pdf", detail: "24 pages - indexed" },
  { name: "Access_Control_Standard.pdf", type: "pdf", detail: "12 pages - indexed" },
  { name: "SOC_2_Type_II_2025.pdf", type: "pdf", detail: "86 pages - indexed" },
  { name: "Incident_Response_Plan.docx", type: "doc", detail: "18 pages - indexed" },
  { name: "Data_Retention_Schedule.xlsx", type: "xlsx", detail: "9 sheets - indexed" },
  { name: "Subprocessor_Register.xlsx", type: "xlsx", detail: "31 records - indexed" },
];

const DEMO_QUESTIONS = [
  {
    id: "q-ac-01",
    number: "AC-01",
    category: "Access control",
    text: "Do you enforce multi-factor authentication for all privileged and administrative access?",
    answer:
      "Yes. Multi-factor authentication is required for all privileged and administrative access to production systems, cloud consoles, and corporate identity services. Access is provisioned through role-based groups, reviewed quarterly, and revoked through the documented offboarding workflow.",
    status: "needs-review",
    coverage: 92,
    claims: 3,
    citations: [
      {
        source: "Access_Control_Standard.pdf",
        location: "Section 4.2 - page 6",
        quote:
          "All privileged accounts, including production administrators and cloud console operators, must authenticate using an approved multi-factor method.",
      },
      {
        source: "SOC_2_Type_II_2025.pdf",
        location: "CC6.2 - page 41",
        quote:
          "The auditor inspected evidence of quarterly privileged access reviews and verified timely removal for sampled terminated users.",
      },
    ],
    flags: [],
    note: "",
  },
  {
    id: "q-ac-02",
    number: "AC-02",
    category: "Access control",
    text: "Describe how user access is approved, reviewed, and revoked.",
    answer:
      "Managers submit access requests through the service desk, and system owners approve access according to job responsibilities. Privileged access is reviewed quarterly, while standard application access is reviewed at least annually. HR termination events trigger same-day deprovisioning through the identity provider.",
    status: "approved",
    coverage: 95,
    claims: 4,
    citations: [
      {
        source: "Access_Control_Standard.pdf",
        location: "Sections 3.1-3.4 - pages 3-5",
        quote:
          "Access requires manager and asset-owner approval. Privileged entitlements are recertified quarterly and removed immediately upon termination notification.",
      },
      {
        source: "SOC_2_Type_II_2025.pdf",
        location: "CC6.1 - page 38",
        quote: "No exceptions were identified in the auditor's sample of new-hire and termination access events.",
      },
    ],
    flags: [],
    note: "Confirmed with IT owner on 2026-08-08.",
  },
  {
    id: "q-dp-01",
    number: "DP-01",
    category: "Data protection",
    text: "Is customer data encrypted in transit and at rest? Specify the standards used.",
    answer:
      "Yes. Customer data is encrypted in transit using TLS 1.2 or higher and at rest using AES-256 encryption provided by the underlying cloud platform. Encryption keys are managed in the cloud key management service with access restricted to authorized platform roles.",
    status: "approved",
    coverage: 97,
    claims: 3,
    citations: [
      {
        source: "Information_Security_Policy.pdf",
        location: "Section 7.3 - page 14",
        quote:
          "Confidential data must use TLS 1.2 or higher during transmission and AES-256 or an equivalent approved control when stored.",
      },
      {
        source: "SOC_2_Type_II_2025.pdf",
        location: "CC6.7 - page 49",
        quote: "Encryption configuration and key-management access were inspected with no exceptions noted.",
      },
    ],
    flags: [],
    note: "",
  },
  {
    id: "q-dp-02",
    number: "DP-02",
    category: "Data protection",
    text: "What is your standard retention period for customer data after contract termination?",
    answer:
      "The evidence library defines retention periods by data class, but it does not establish a single default period for all customer data after contract termination. The applicable period should be confirmed against the customer agreement and deletion procedure before a final response is provided.",
    status: "draft",
    coverage: 54,
    claims: 1,
    citations: [
      {
        source: "Data_Retention_Schedule.xlsx",
        location: "Customer Data sheet - rows 8-14",
        quote:
          "Retention varies by record category; contractual commitments and legal holds may supersede the baseline schedule.",
      },
    ],
    flags: [
      {
        type: "missing",
        title: "Missing evidence",
        detail: "No approved deletion procedure or universal post-termination retention period was found.",
      },
    ],
    note: "Ask Legal to provide the standard DPA deletion commitment.",
  },
  {
    id: "q-ir-01",
    number: "IR-01",
    category: "Incident response",
    text: "Do you maintain and test a documented incident response plan?",
    answer:
      "Yes. A documented incident response plan assigns severity levels, response roles, escalation paths, evidence-preservation requirements, and communication responsibilities. The plan is reviewed annually and exercised through at least one tabletop test each year.",
    status: "approved",
    coverage: 94,
    claims: 3,
    citations: [
      {
        source: "Incident_Response_Plan.docx",
        location: "Sections 2-6 - pages 3-13",
        quote:
          "The Incident Commander coordinates containment, investigation, evidence preservation, recovery, and stakeholder communications by assigned severity level.",
      },
      {
        source: "SOC_2_Type_II_2025.pdf",
        location: "CC7.4 - page 62",
        quote: "Management provided the annual tabletop exercise record; no control exceptions were identified.",
      },
    ],
    flags: [],
    note: "",
  },
  {
    id: "q-ir-02",
    number: "IR-02",
    category: "Incident response",
    text: "Within how many hours will you notify customers of a confirmed security incident?",
    answer:
      "The incident response plan requires prompt customer notification following confirmation and impact assessment. The current evidence does not support a universal notification window; the governing customer agreement and applicable law determine the deadline.",
    status: "needs-review",
    coverage: 66,
    claims: 2,
    citations: [
      {
        source: "Incident_Response_Plan.docx",
        location: "Section 6.4 - page 14",
        quote:
          "Legal and the Incident Commander determine external notification timing based on contractual and regulatory obligations.",
      },
    ],
    flags: [
      {
        type: "contradiction",
        title: "Conflicting source language",
        detail: "A legacy policy appendix references 72 hours, while the current response plan defers to contract terms.",
      },
    ],
    note: "Use contract-specific language. Do not claim a universal 72-hour commitment.",
  },
  {
    id: "q-bc-01",
    number: "BC-01",
    category: "Resilience",
    text: "How often are business continuity and disaster recovery plans tested?",
    answer:
      "Business continuity and disaster recovery plans are tested at least annually. Material findings are recorded, assigned to owners, and tracked through remediation. Recovery objectives are reviewed as part of the exercise process.",
    status: "approved",
    coverage: 90,
    claims: 3,
    citations: [
      {
        source: "Information_Security_Policy.pdf",
        location: "Section 10.2 - page 20",
        quote:
          "Business continuity and disaster recovery exercises will occur no less than annually, with remediation tracked to closure.",
      },
    ],
    flags: [],
    note: "",
  },
  {
    id: "q-vm-01",
    number: "VM-01",
    category: "Vulnerability management",
    text: "Describe your vulnerability scanning and remediation program.",
    answer:
      "Authenticated infrastructure and application vulnerability scans run at least monthly, with additional scanning after material changes. Critical findings are targeted for remediation within 15 days and high findings within 30 days, subject to documented risk acceptance and compensating controls.",
    status: "approved",
    coverage: 93,
    claims: 4,
    citations: [
      {
        source: "Information_Security_Policy.pdf",
        location: "Section 8.4 - pages 16-17",
        quote:
          "Monthly scanning is required. Critical vulnerabilities have a 15-day target and high vulnerabilities have a 30-day target unless formally excepted.",
      },
      {
        source: "SOC_2_Type_II_2025.pdf",
        location: "CC7.1 - page 55",
        quote: "Sampled findings were remediated or risk accepted within the established service levels.",
      },
    ],
    flags: [],
    note: "",
  },
  {
    id: "q-tp-01",
    number: "TP-01",
    category: "Third parties",
    text: "Provide a current list of subprocessors that may process customer personal data.",
    answer:
      "The current evidence register identifies 31 subprocessors and records service purpose, processing location, data category, and review owner. Confirm that the register is approved for external disclosure before attaching it to the final response.",
    status: "needs-review",
    coverage: 78,
    claims: 2,
    citations: [
      {
        source: "Subprocessor_Register.xlsx",
        location: "Current Register - rows 2-32",
        quote: "31 active entries include provider, purpose, processing region, data class, and review date.",
      },
    ],
    flags: [
      {
        type: "missing",
        title: "Approval required",
        detail: "The register is marked Internal and has no external-disclosure approval attached.",
      },
    ],
    note: "Privacy team to approve the customer-facing register.",
  },
  {
    id: "q-gr-01",
    number: "GR-01",
    category: "Logging & monitoring",
    text: "How long are security audit logs retained and who can access them?",
    answer:
      "Security audit logs are retained for 365 days, with at least 90 days available for immediate search. Access is limited to authorized Security and Platform Engineering roles and is itself logged and reviewed.",
    status: "approved",
    coverage: 88,
    claims: 3,
    citations: [
      {
        source: "Information_Security_Policy.pdf",
        location: "Section 9.3 - page 18",
        quote:
          "Security logs are retained for 365 days, including 90 days in the searchable tier. Access is restricted to approved security and platform roles.",
      },
    ],
    flags: [],
    note: "",
  },
  {
    id: "q-hr-01",
    number: "HR-01",
    category: "Personnel security",
    text: "Are background checks completed for all employees and contractors before access is granted?",
    answer:
      "Background screening is completed for employees where permitted by local law and proportionate to the role. The current evidence does not establish that the same control applies to every contractor before access is granted.",
    status: "rejected",
    coverage: 61,
    claims: 2,
    citations: [
      {
        source: "Information_Security_Policy.pdf",
        location: "Section 4.1 - page 7",
        quote: "Personnel screening is conducted where lawful and appropriate for the responsibilities of the role.",
      },
    ],
    flags: [
      {
        type: "missing",
        title: "Contractor coverage not evidenced",
        detail: "No source confirms pre-access screening for all contractor populations.",
      },
    ],
    note: "Rejected pending People Ops confirmation for contractors.",
  },
  {
    id: "q-ai-01",
    number: "AI-01",
    category: "AI governance",
    text: "Is customer data used to train shared or public artificial intelligence models?",
    answer:
      "No supported answer is available from the current evidence library. Obtain the approved AI data-use policy and product architecture statement before responding.",
    status: "draft",
    coverage: 28,
    claims: 0,
    citations: [],
    flags: [
      {
        type: "missing",
        title: "No supporting evidence found",
        detail: "The indexed policy set does not describe model training or customer-data use for AI features.",
      },
    ],
    note: "Route to Product and Legal. Do not infer from general privacy language.",
  },
];

const STATUS_LABELS = {
  draft: "Draft",
  "needs-review": "Needs review",
  approved: "Approved",
  rejected: "Rejected",
};

const state = {
  questions: DEMO_QUESTIONS.map((question) => structuredClone(question)),
  evidence: DEMO_EVIDENCE.map((file) => ({ ...file })),
  selectedId: DEMO_QUESTIONS[0].id,
  projectId: null,
  demoMode: true,
  search: "",
  filters: new Set(Object.keys(STATUS_LABELS)),
  running: false,
  saveTimer: null,
  backendConnected: false,
  providerLabel: "Evidence-only demo",
};

const dom = {};

document.addEventListener("DOMContentLoaded", () => {
  cacheDom();
  bindEvents();
  renderEvidence();
  renderAll();
  refreshIcons();
  hydrateFromApi();
});

function cacheDom() {
  [
    "projectName",
    "saveState",
    "toggleSources",
    "closeSources",
    "sourcePanel",
    "drawerScrim",
    "questionnaireInput",
    "questionnaireDropzone",
    "questionnaireFile",
    "evidenceInput",
    "evidenceList",
    "evidenceCount",
    "runButton",
    "pipeline",
    "runTimestamp",
    "providerState",
    "questionCount",
    "statusSummary",
    "searchInput",
    "filterButton",
    "filterIndicator",
    "filterMenu",
    "clearFilters",
    "questionList",
    "emptyState",
    "collapseQueue",
    "reviewPanel",
    "backToQueue",
    "questionPosition",
    "questionStatus",
    "previousQuestion",
    "nextQuestion",
    "reviewScroll",
    "questionCategory",
    "questionId",
    "questionText",
    "coverageBadge",
    "coverageValue",
    "answerEditor",
    "wordCount",
    "regenerateButton",
    "claimCount",
    "flagList",
    "citationList",
    "reviewerNote",
    "rejectButton",
    "approveButton",
    "rejectDialog",
    "rejectForm",
    "rejectionReason",
    "exportButton",
    "exportDialog",
    "exportForm",
    "includeDrafts",
    "toastRegion",
  ].forEach((id) => {
    dom[id] = document.getElementById(id);
  });
}

function bindEvents() {
  dom.searchInput.addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderQueue();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && !isTypingTarget(event.target)) {
      event.preventDefault();
      dom.searchInput.focus();
    }
    if (event.key === "Escape") {
      dom.filterMenu.hidden = true;
      dom.filterButton.setAttribute("aria-expanded", "false");
      closeSourceDrawer();
    }
  });

  dom.filterButton.addEventListener("click", (event) => {
    event.stopPropagation();
    dom.filterMenu.hidden = !dom.filterMenu.hidden;
    dom.filterButton.setAttribute("aria-expanded", String(!dom.filterMenu.hidden));
  });

  dom.filterMenu.addEventListener("click", (event) => event.stopPropagation());
  document.addEventListener("click", () => {
    dom.filterMenu.hidden = true;
    dom.filterButton.setAttribute("aria-expanded", "false");
  });

  dom.filterMenu.querySelectorAll('input[type="checkbox"]').forEach((input) => {
    input.addEventListener("change", () => {
      if (input.checked) state.filters.add(input.value);
      else state.filters.delete(input.value);
      state.flaggedOnly = false;
      updateFilterIndicator();
      renderQueue();
    });
  });

  dom.clearFilters.addEventListener("click", () => {
    state.filters = new Set(Object.keys(STATUS_LABELS));
    state.flaggedOnly = false;
    dom.filterMenu.querySelectorAll('input[type="checkbox"]').forEach((input) => {
      input.checked = true;
    });
    updateFilterIndicator();
    renderQueue();
  });

  dom.answerEditor.addEventListener("input", () => {
    const question = selectedQuestion();
    if (!question) return;
    question.answer = dom.answerEditor.value;
    if (question.status === "approved") question.status = "needs-review";
    updateWordCount();
    scheduleSave(question);
    renderStatusSummary();
  });

  dom.reviewerNote.addEventListener("input", () => {
    const question = selectedQuestion();
    if (!question) return;
    question.note = dom.reviewerNote.value;
    scheduleSave(question);
  });

  dom.approveButton.addEventListener("click", () => setDecision("approved"));
  dom.rejectButton.addEventListener("click", () => {
    dom.rejectionReason.value = selectedQuestion()?.note || "";
    dom.rejectDialog.showModal();
    setTimeout(() => dom.rejectionReason.focus(), 0);
  });

  dom.rejectForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (event.submitter?.value === "confirm") {
      if (!dom.rejectionReason.value.trim()) {
        dom.rejectionReason.setCustomValidity("Add a reason for rejection.");
        dom.rejectionReason.reportValidity();
        return;
      }
      dom.rejectionReason.setCustomValidity("");
      const question = selectedQuestion();
      if (question) question.note = dom.rejectionReason.value.trim();
      setDecision("rejected");
    }
    dom.rejectDialog.close();
  });

  dom.previousQuestion.addEventListener("click", () => moveSelection(-1));
  dom.nextQuestion.addEventListener("click", () => moveSelection(1));
  dom.backToQueue.addEventListener("click", () => document.body.classList.remove("mobile-review"));
  dom.regenerateButton.addEventListener("click", regenerateAnswer);

  dom.runButton.addEventListener("click", runPipeline);
  dom.questionnaireInput.addEventListener("change", () => handleQuestionnaire(dom.questionnaireInput.files[0]));
  dom.questionnaireFile.addEventListener("click", (event) => {
    if (!event.target.closest("button")) return;
    dom.questionnaireFile.hidden = true;
    dom.questionnaireInput.value = "";
    showToast("Questionnaire removed", "warning");
  });
  dom.evidenceInput.addEventListener("change", () => handleEvidenceFiles([...dom.evidenceInput.files]));
  bindDropzone();

  dom.toggleSources.addEventListener("click", openSourceDrawer);
  dom.closeSources.addEventListener("click", closeSourceDrawer);
  dom.drawerScrim.addEventListener("click", closeSourceDrawer);

  dom.collapseQueue.addEventListener("click", () => document.body.classList.toggle("queue-collapsed"));
  dom.reviewPanel.addEventListener("click", (event) => {
    if (document.body.classList.contains("queue-collapsed") && event.clientX < 32) {
      document.body.classList.remove("queue-collapsed");
    }
  });

  dom.exportButton.addEventListener("click", () => dom.exportDialog.showModal());
  dom.exportForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (event.submitter?.value === "confirm") exportResponses();
    dom.exportDialog.close();
  });
}

async function hydrateFromApi() {
  const health = await apiRequest("/api/health", { method: "GET" });
  if (health?.provider?.active) {
    state.providerLabel = health.provider.active === "deterministic-demo" ? "Evidence-only demo" : "Strands provider";
    renderProviderState();
  }
  const projects = await apiRequest("/api/projects", { method: "GET" });
  if (!Array.isArray(projects) || projects.length === 0) return;
  await loadProject(projects[0].id);
}

async function loadProject(projectId) {
  const payload = await apiRequest(`/api/projects/${encodeURIComponent(projectId)}`, { method: "GET" });
  if (!payload?.project) return false;

  state.projectId = payload.project.id;
  state.demoMode = false;
  state.questions = (payload.questions ?? []).map(normalizeQuestion);
  state.selectedId = state.questions[0]?.id ?? null;
  state.evidence = (payload.documents ?? []).filter((document) => document.kind === "evidence").map(normalizeEvidence);
  state.backendConnected = true;
  renderProviderState();
  dom.projectName.textContent = payload.project.name;

  const questionnaire = (payload.documents ?? []).find((document) => document.kind === "questionnaire");
  if (questionnaire) renderQuestionnaireRecord(questionnaire, state.questions.length);
  renderEvidence();
  renderAll();
  showToast("Live workspace loaded", "success");
  return true;
}

async function ensureProject() {
  if (state.projectId) return state.projectId;
  const project = await apiRequest("/api/projects", {
    method: "POST",
    body: JSON.stringify({ name: dom.projectName.textContent || "EvidenceOps Review" }),
  });
  if (!project?.id) return null;

  state.projectId = project.id;
  state.demoMode = false;
  state.questions = [];
  state.evidence = [];
  state.selectedId = null;
  renderEvidence();
  renderAll();
  return project.id;
}

function normalizeQuestion(question, index) {
  const inferredCoverage = question.checks?.grounded
    ? question.checks?.hallucination_risk
      ? 72
      : 92
    : question.citations?.length
      ? 64
      : 28;
  const rawCoverage = Number(question.coverage ?? question.confidence ?? question.confidence_score ?? inferredCoverage);
  const coverage = rawCoverage > 0 && rawCoverage <= 1 ? Math.round(rawCoverage * 100) : Math.round(rawCoverage);
  const flags = Array.isArray(question.flags) ? [...question.flags] : [];

  const contradictions = question.checks?.contradictions ?? question.contradictions;
  if (Array.isArray(contradictions)) {
    contradictions.forEach((detail) =>
      flags.push({
        type: "contradiction",
        title: "Conflicting evidence",
        detail: typeof detail === "object" ? detail.summary ?? JSON.stringify(detail) : String(detail),
      }),
    );
  }
  if (question.checks?.hallucination_risk && !flags.some((flag) => flag.type === "contradiction")) {
    flags.push({
      type: "contradiction",
      title: "Grounding check requires review",
      detail: question.checks.unsupported_claims?.join(" ") || "One or more claims require stronger citation support.",
    });
  }
  if (typeof question.missing_evidence === "string" && question.missing_evidence) {
    flags.push({ type: "missing", title: "Missing evidence", detail: question.missing_evidence });
  } else if (Array.isArray(question.missing_evidence)) {
    question.missing_evidence.forEach((detail) =>
      flags.push({ type: "missing", title: "Missing evidence", detail: String(detail) }),
    );
  }

  return {
    id: String(question.id ?? question.question_id ?? `question-${index + 1}`),
    number: String(question.number ?? question.display_id ?? question.control_id ?? `Q-${String(index + 1).padStart(2, "0")}`),
    category: question.category ?? question.section ?? question.source_document ?? "General",
    text: question.text ?? question.question ?? question.question_text ?? "Untitled question",
    answer: question.answer ?? question.draft_answer ?? question.proposed_answer ?? "",
    status: normalizeStatus(question.status),
    coverage: Number.isFinite(coverage) ? Math.max(0, Math.min(100, coverage)) : 0,
    claims: Number(question.claims ?? question.verified_claims ?? 0),
    citationsLinked: question.citations?.length ?? question.evidence?.length ?? 0,
    citations: (question.citations ?? question.evidence ?? []).map(normalizeCitation),
    flags,
    note: question.note ?? question.reviewer_note ?? "",
  };
}

function normalizeStatus(value) {
  const normalized = String(value ?? "draft")
    .toLowerCase()
    .replaceAll("_", "-")
    .replaceAll(" ", "-");
  if (normalized === "review" || normalized === "pending-review") return "needs-review";
  if (normalized === "needs-evidence") return "needs-review";
  if (normalized === "pending") return "draft";
  return STATUS_LABELS[normalized] ? normalized : "draft";
}

function normalizeCitation(citation, index) {
  return {
    source: citation.source ?? citation.source_name ?? citation.document ?? `Evidence ${index + 1}`,
    location:
      citation.location ??
      citation.page_or_sheet ??
      ([citation.section, citation.page_number ? `page ${citation.page_number}` : null].filter(Boolean).join(" - ") ||
        "Referenced excerpt"),
    quote: citation.quote ?? citation.excerpt ?? citation.text ?? "Evidence excerpt available in the source document.",
  };
}

function normalizeEvidence(file) {
  const name = file.name ?? file.filename ?? "Evidence file";
  const excerptCount = Number(file.chunk_count ?? 0);
  return {
    name,
    type: file.type ?? fileExtension(name),
    detail:
      file.detail ?? file.status ?? `${excerptCount} ${excerptCount === 1 ? "excerpt" : "excerpts"} - indexed`,
  };
}

function renderAll() {
  renderProviderState();
  renderStatusSummary();
  renderQueue();
  renderReview();
  if (!state.running) renderPipelineSummary();
  dom.questionCount.textContent = state.questions.length;
}

function renderProviderState() {
  if (!dom.providerState) return;
  const label = state.providerLabel || (state.backendConnected ? "Service ready" : "Offline");
  dom.providerState.innerHTML = `<span></span> ${escapeHtml(label)}`;
  dom.providerState.title = label === "Strands provider"
    ? "Operator-configured Strands provider is available for drafting"
    : "Drafts remain constrained to retrieved evidence when no hosted provider is configured";
}

function renderPipelineSummary() {
  const total = state.questions.length;
  const evidenced = state.questions.filter((question) => question.citations.length > 0).length;
  const drafted = state.questions.filter((question) => question.answer.trim()).length;
  const flagged = state.questions.filter((question) => question.flags.length > 0).length;
  const hasRun = evidenced > 0 || drafted > 0 || flagged > 0;
  const rows = [
    { label: "Extract questions", value: total, complete: total > 0 },
    { label: "Retrieve evidence", value: hasRun ? evidenced : "Waiting", complete: hasRun },
    { label: "Draft answers", value: hasRun ? drafted : "Waiting", complete: hasRun },
    { label: "Verify claims", value: hasRun ? `${flagged} flags` : "Waiting", complete: hasRun },
  ];

  dom.pipeline.innerHTML = rows
    .map(
      (row) => `
        <li class="${row.complete ? "complete" : ""}">
          <i data-lucide="${row.complete ? "check" : "circle"}"></i>
          <span>${row.label}</span><small>${row.value}</small>
        </li>
      `,
    )
    .join("");

  dom.runButton.disabled = total === 0;
  dom.runButton.innerHTML = `<i data-lucide="${hasRun ? "rotate-cw" : "play"}"></i><span>${hasRun ? "Run again" : "Run questionnaire"}</span>`;
  if (state.demoMode) dom.runTimestamp.textContent = "Synthetic demo dataset";
  else if (hasRun) dom.runTimestamp.textContent = "Saved run loaded";
  else dom.runTimestamp.textContent = "Ready after evidence upload";
  refreshIcons();
}

function renderStatusSummary() {
  const counts = {
    total: state.questions.length,
    review: state.questions.filter((question) => question.status === "needs-review").length,
    approved: state.questions.filter((question) => question.status === "approved").length,
    flagged: state.questions.filter((question) => question.flags.length > 0).length,
  };

  dom.statusSummary.innerHTML = `
    <button class="status-stat active" type="button" data-summary="all"><strong>${counts.total}</strong><span>All</span></button>
    <button class="status-stat review" type="button" data-summary="needs-review"><strong>${counts.review}</strong><span>Review</span></button>
    <button class="status-stat approved" type="button" data-summary="approved"><strong>${counts.approved}</strong><span>Approved</span></button>
    <button class="status-stat flagged" type="button" data-summary="flagged"><strong>${counts.flagged}</strong><span>Flagged</span></button>
  `;

  dom.statusSummary.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => applySummaryFilter(button.dataset.summary));
  });
}

function applySummaryFilter(summary) {
  dom.statusSummary.querySelectorAll("button").forEach((button) => {
    button.classList.toggle("active", button.dataset.summary === summary);
  });

  if (summary === "all") {
    state.filters = new Set(Object.keys(STATUS_LABELS));
    state.flaggedOnly = false;
  } else if (summary === "flagged") {
    state.filters = new Set(Object.keys(STATUS_LABELS));
    state.flaggedOnly = true;
  } else {
    state.filters = new Set([summary]);
    state.flaggedOnly = false;
  }

  dom.filterMenu.querySelectorAll('input[type="checkbox"]').forEach((input) => {
    input.checked = state.filters.has(input.value);
  });
  updateFilterIndicator();
  renderQueue();
}

function renderQueue() {
  const questions = filteredQuestions();
  dom.questionList.innerHTML = "";
  dom.emptyState.hidden = questions.length !== 0;

  questions.forEach((question) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `question-item${question.id === state.selectedId ? " selected" : ""}`;
    button.dataset.id = question.id;
    button.setAttribute("role", "option");
    button.setAttribute("aria-selected", String(question.id === state.selectedId));
    const flagMarkup = question.flags
      .slice(0, 1)
      .map((flag) => {
        const icon = flag.type === "contradiction" ? "git-compare-arrows" : "file-question";
        return `<span class="mini-flag ${flag.type === "missing" ? "missing" : ""}"><i data-lucide="${icon}"></i>${
          flag.type === "contradiction" ? "Conflict" : "Missing"
        }</span>`;
      })
      .join("");

    button.innerHTML = `
      <span class="question-item-top">
        <span class="question-number">${escapeHtml(question.number)}</span>
        <span class="question-category">${escapeHtml(question.category)}</span>
      </span>
      <p>${escapeHtml(question.text)}</p>
      <span class="queue-status ${question.status}">${STATUS_LABELS[question.status]}</span>
      <span class="question-item-flags">${flagMarkup}<span class="queue-confidence" aria-label="${question.coverage}% evidence coverage">${question.coverage}%</span></span>
    `;
    button.addEventListener("click", () => selectQuestion(question.id));
    dom.questionList.appendChild(button);
  });

  refreshIcons();
}

function renderReview() {
  const question = selectedQuestion();
  if (!question) {
    dom.questionPosition.textContent = "No question selected";
    dom.questionStatus.className = "status-badge status-draft";
    dom.questionStatus.textContent = "Waiting";
    dom.questionCategory.textContent = "Workspace";
    dom.questionId.textContent = "--";
    dom.questionText.textContent = "Upload a questionnaire or add questions to begin.";
    dom.answerEditor.value = "";
    dom.answerEditor.placeholder = "An evidence-backed draft will appear here after the agent run.";
    dom.answerEditor.disabled = true;
    dom.reviewerNote.value = "";
    dom.reviewerNote.disabled = true;
    dom.coverageValue.textContent = "0%";
    dom.coverageBadge.className = "confidence low";
    dom.claimCount.textContent = "0 citations linked";
    dom.flagList.innerHTML = "";
    dom.citationList.innerHTML = "";
    dom.previousQuestion.disabled = true;
    dom.nextQuestion.disabled = true;
    dom.approveButton.disabled = true;
    dom.rejectButton.disabled = true;
    updateWordCount();
    return;
  }
  dom.answerEditor.disabled = false;
  dom.answerEditor.placeholder = "";
  dom.reviewerNote.disabled = false;
  dom.rejectButton.disabled = false;
  const index = state.questions.findIndex((item) => item.id === question.id);

  dom.questionPosition.textContent = `Question ${index + 1} of ${state.questions.length}`;
  dom.questionStatus.className = `status-badge status-${question.status}`;
  dom.questionStatus.textContent = STATUS_LABELS[question.status];
  dom.questionCategory.textContent = question.category;
  dom.questionId.textContent = question.number;
  dom.questionText.textContent = question.text;
  dom.answerEditor.value = question.answer;
  dom.reviewerNote.value = question.note;
  dom.coverageValue.textContent = `${question.coverage}%`;
  dom.coverageBadge.className = `confidence${question.coverage < 50 ? " low" : question.coverage < 80 ? " medium" : ""}`;
  const linked = question.citationsLinked ?? question.citations.length;
  dom.claimCount.textContent = `${linked} ${linked === 1 ? "citation" : "citations"} linked`;
  dom.previousQuestion.disabled = index <= 0;
  dom.nextQuestion.disabled = index >= state.questions.length - 1;
  dom.approveButton.innerHTML = `<i data-lucide="check"></i> ${question.status === "approved" ? "Approved" : "Approve"}`;
  dom.approveButton.disabled = question.status === "approved";
  renderFlags(question);
  renderCitations(question);
  updateWordCount();
  refreshIcons();
}

function renderFlags(question) {
  dom.flagList.innerHTML = question.flags
    .map((flag) => {
      const isMissing = flag.type === "missing";
      return `
        <div class="verification-flag ${isMissing ? "missing" : ""}">
          <i data-lucide="${isMissing ? "file-question" : "git-compare-arrows"}"></i>
          <div><strong>${escapeHtml(flag.title)}</strong><span>${escapeHtml(flag.detail)}</span></div>
        </div>
      `;
    })
    .join("");
}

function renderCitations(question) {
  if (question.citations.length === 0) {
    dom.citationList.innerHTML = `
      <div class="verification-flag missing">
        <i data-lucide="book-x"></i>
        <div><strong>No citation attached</strong><span>This draft must not be approved until supporting evidence is linked.</span></div>
      </div>
    `;
    return;
  }

  dom.citationList.innerHTML = question.citations
    .map(
      (citation, index) => `
        <article class="citation">
          <div class="citation-header">
            <span class="citation-number">${index + 1}</span>
            <strong>${escapeHtml(citation.source)}</strong>
            <span>${escapeHtml(citation.location)}</span>
            <button type="button" aria-label="Open ${escapeHtml(citation.source)}" title="Open source"><i data-lucide="external-link"></i></button>
          </div>
          <blockquote>&ldquo;${escapeHtml(citation.quote)}&rdquo;</blockquote>
        </article>
      `,
    )
    .join("");

  dom.citationList.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => showToast("Source preview is available when connected to the document store.", "warning"));
  });
}

function renderEvidence() {
  dom.evidenceCount.textContent = `${state.evidence.length} ${state.evidence.length === 1 ? "source" : "sources"} indexed`;
  dom.evidenceList.innerHTML = state.evidence
    .map(
      (file) => `
        <div class="file-row">
          <span class="file-type ${safeClass(file.type)}">${fileTypeLabel(file.type)}</span>
          <span class="file-meta"><strong title="${escapeHtml(file.name)}">${escapeHtml(file.name)}</strong><small>${escapeHtml(
            file.detail,
          )}</small></span>
          <i class="file-indexed" data-lucide="circle-check" aria-label="Indexed"></i>
        </div>
      `,
    )
    .join("");
  refreshIcons();
}

function renderQuestionnaireRecord(documentRecord, questionCount) {
  const name = documentRecord.filename ?? documentRecord.name ?? "Questionnaire";
  const type = fileExtension(name);
  dom.questionnaireFile.hidden = false;
  dom.questionnaireFile.innerHTML = `
    <span class="file-type ${safeClass(type)}">${fileTypeLabel(type)}</span>
    <span class="file-meta"><strong>${escapeHtml(name)}</strong><small>${questionCount} ${
      questionCount === 1 ? "question" : "questions"
    } - indexed</small></span>
    <button class="icon-button compact" type="button" aria-label="Remove questionnaire" title="Remove"><i data-lucide="x"></i></button>
  `;
  refreshIcons();
}

function selectQuestion(id) {
  state.selectedId = id;
  renderQueue();
  renderReview();
  dom.reviewScroll.scrollTop = 0;
  document.body.classList.add("mobile-review");
}

function moveSelection(offset) {
  const questions = filteredQuestions();
  const index = questions.findIndex((question) => question.id === state.selectedId);
  const next = questions[index + offset];
  if (next) selectQuestion(next.id);
}

function selectedQuestion() {
  return state.questions.find((question) => question.id === state.selectedId);
}

function filteredQuestions() {
  return state.questions.filter((question) => {
    const matchesStatus = state.filters.has(question.status);
    const matchesFlag = !state.flaggedOnly || question.flags.length > 0;
    const haystack = `${question.number} ${question.category} ${question.text} ${question.answer}`.toLowerCase();
    return matchesStatus && matchesFlag && (!state.search || haystack.includes(state.search));
  });
}

function updateFilterIndicator() {
  const allStatuses = state.filters.size === Object.keys(STATUS_LABELS).length;
  dom.filterIndicator.hidden = allStatuses && !state.flaggedOnly;
}

function updateWordCount() {
  const words = dom.answerEditor.value.trim() ? dom.answerEditor.value.trim().split(/\s+/).length : 0;
  dom.wordCount.textContent = `${words} ${words === 1 ? "word" : "words"}`;
}

function scheduleSave(question) {
  window.clearTimeout(state.saveTimer);
  dom.saveState.innerHTML = '<i data-lucide="cloud-upload"></i> Saving changes...';
  refreshIcons();
  state.saveTimer = window.setTimeout(async () => {
    if (state.projectId) {
      const saved = await apiRequest(
        `/api/projects/${encodeURIComponent(state.projectId)}/questions/${encodeURIComponent(question.id)}`,
        {
          method: "PATCH",
          body: JSON.stringify({ edited_answer: question.answer, note: question.note || null }),
        },
      );
      if (!saved || saved._error) {
        dom.saveState.innerHTML = '<i data-lucide="cloud-off"></i> Save pending';
        refreshIcons();
        return;
      }
      const index = state.questions.findIndex((item) => item.id === question.id);
      if (index >= 0) {
        const updated = normalizeQuestion(saved, index);
        state.questions.splice(index, 1, updated);
        state.selectedId = updated.id;
      }
    }
    dom.saveState.innerHTML = '<i data-lucide="circle-check"></i> All changes saved';
    refreshIcons();
    renderQueue();
    renderReview();
  }, 650);
}

async function setDecision(status) {
  const question = selectedQuestion();
  if (!question) return;

  if (status === "approved" && (question.citations.length === 0 || question.flags.some((flag) => flag.type === "missing"))) {
    showToast("Review the missing-evidence warning before approval.", "warning");
    return;
  }

  if (state.projectId) {
    const result = await reviewQuestion(question, status);
    if (result?._error) {
      showToast(result.detail || "The evidence check blocked this review decision.", "warning");
      return;
    }
    if (result) {
      const updated = normalizeQuestion(result, state.questions.indexOf(question));
      state.questions.splice(state.questions.indexOf(question), 1, updated);
      state.selectedId = updated.id;
    } else {
      showToast("The review service did not respond. Your edit remains in this session.", "warning");
      return;
    }
  } else {
    question.status = status;
  }
  renderAll();
  showToast(status === "approved" ? "Answer approved for export" : "Answer returned for revision", status === "approved" ? "success" : "warning");
}

async function reviewQuestion(question, status) {
  const path = `/api/projects/${encodeURIComponent(state.projectId)}/questions/${encodeURIComponent(question.id)}/review`;
  return apiRequest(path, {
    method: "PATCH",
    body: JSON.stringify({
      action: status === "approved" ? "approve" : "reject",
      edited_answer: question.answer,
      note: question.note || null,
    }),
  });
}

async function regenerateAnswer() {
  const question = selectedQuestion();
  if (!question) return;
  dom.regenerateButton.disabled = true;
  dom.regenerateButton.innerHTML = '<span class="step-spinner"></span> Regenerating';

  const payload = state.projectId
    ? await apiRequest(`/api/projects/${encodeURIComponent(state.projectId)}/run`, { method: "POST", timeoutMs: 90000 })
    : null;
  const refreshed = payload?.questions?.find((item) => String(item.id) === question.id);
  if (refreshed) {
    const updated = normalizeQuestion(refreshed, state.questions.indexOf(question));
    state.questions.splice(state.questions.indexOf(question), 1, updated);
    state.selectedId = updated.id;
    showToast("Draft regenerated from indexed evidence", "success");
  } else {
    showToast("Draft preserved. Add evidence or connect a model provider to regenerate.", "warning");
  }

  dom.regenerateButton.disabled = false;
  dom.regenerateButton.innerHTML = '<i data-lucide="refresh-cw"></i> Regenerate';
  renderAll();
}

function bindDropzone() {
  ["dragenter", "dragover"].forEach((type) => {
    dom.questionnaireDropzone.addEventListener(type, (event) => {
      event.preventDefault();
      dom.questionnaireDropzone.classList.add("dragging");
    });
  });
  ["dragleave", "drop"].forEach((type) => {
    dom.questionnaireDropzone.addEventListener(type, (event) => {
      event.preventDefault();
      dom.questionnaireDropzone.classList.remove("dragging");
    });
  });
  dom.questionnaireDropzone.addEventListener("drop", (event) => handleQuestionnaire(event.dataTransfer.files[0]));
  dom.questionnaireDropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      dom.questionnaireInput.click();
    }
  });
}

async function handleQuestionnaire(file) {
  if (!file) return;
  dom.questionnaireFile.hidden = false;
  dom.questionnaireFile.innerHTML = `
    <span class="file-type ${safeClass(fileExtension(file.name))}">${fileTypeLabel(fileExtension(file.name))}</span>
    <span class="file-meta"><strong>${escapeHtml(file.name)}</strong><small>${formatBytes(file.size)} - ready to process</small></span>
    <button class="icon-button compact" type="button" aria-label="Remove questionnaire" title="Remove"><i data-lucide="x"></i></button>
  `;
  refreshIcons();
  const projectId = await ensureProject();
  if (!projectId) {
    showToast("The local API is offline. The file remains selected for this session.", "warning");
    return;
  }
  const formData = new FormData();
  formData.append("files", file);
  const payload = await apiRequest(
    `/api/projects/${encodeURIComponent(projectId)}/documents?kind=questionnaire`,
    { method: "POST", body: formData, timeoutMs: 60000 },
  );
  if (!payload || payload._error) {
    showToast(payload?.detail || "Questionnaire upload did not complete. The file remains selected.", "warning");
    return;
  }
  const addedQuestions = payload?.uploads?.flatMap((upload) => upload.questions_added ?? []) ?? [];
  if (addedQuestions.length) {
    state.questions = addedQuestions.map(normalizeQuestion);
    state.selectedId = state.questions[0]?.id ?? null;
    renderAll();
  }
  showToast(`${file.name} added as questionnaire`, "success");
}

async function handleEvidenceFiles(files) {
  if (!files.length) return;
  const projectId = await ensureProject();
  files.forEach((file) => {
    state.evidence.push({ name: file.name, type: fileExtension(file.name), detail: `${formatBytes(file.size)} - indexing` });
  });
  renderEvidence();

  if (!projectId) {
    files.forEach((file) => {
      const evidence = state.evidence.find((item) => item.name === file.name);
      if (evidence) evidence.detail = `${formatBytes(file.size)} - queued locally`;
    });
    renderEvidence();
    showToast("The local API is offline. Evidence is queued in this session.", "warning");
    return;
  }

  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  const payload = await apiRequest(`/api/projects/${encodeURIComponent(projectId)}/documents?kind=evidence`, {
    method: "POST",
    body: formData,
    timeoutMs: 60000,
  });

  if (!payload || payload._error) {
    files.forEach((file) => {
      const evidence = state.evidence.find((item) => item.name === file.name);
      if (evidence) evidence.detail = `${formatBytes(file.size)} - upload failed`;
    });
    renderEvidence();
    showToast(payload?.detail || "Evidence upload did not complete.", "warning");
    return;
  }

  files.forEach((file) => {
    const evidence = state.evidence.find((item) => item.name === file.name);
    if (evidence) evidence.detail = payload ? "indexed" : `${formatBytes(file.size)} - queued`;
  });
  renderEvidence();
  showToast(`${files.length} evidence ${files.length === 1 ? "file" : "files"} added`, "success");
}

async function runPipeline() {
  if (state.running) return;
  state.running = true;
  dom.runButton.disabled = true;
  dom.runButton.innerHTML = '<span class="step-spinner"></span><span>Agent running</span>';

  const stages = [
    ["Extract questions", `${state.questions.length}`],
    ["Retrieve evidence", ""],
    ["Draft answers", ""],
    ["Verify claims", ""],
  ];

  for (let index = 0; index < stages.length; index += 1) {
    renderPipeline(stages, index);
    await delay(520);
  }

  const projectId = state.demoMode ? null : await ensureProject();
  const payload = projectId
    ? await apiRequest(`/api/projects/${encodeURIComponent(projectId)}/run`, { method: "POST", timeoutMs: 90000 })
    : null;
  if (payload?._error) {
    dom.runButton.disabled = false;
    dom.runButton.innerHTML = '<i data-lucide="play"></i><span>Retry run</span>';
    state.running = false;
    refreshIcons();
    showToast(payload.detail || "The agent run stopped before producing drafts.", "warning");
    return;
  }
  const incoming = Array.isArray(payload) ? payload : payload?.questions;
  if (Array.isArray(incoming) && incoming.length) {
    state.questions = incoming.map(normalizeQuestion);
    state.selectedId = state.questions[0].id;
    state.backendConnected = true;
  }

  renderPipeline(stages, stages.length);
  dom.runTimestamp.textContent = `Last run today, ${new Intl.DateTimeFormat([], { hour: "2-digit", minute: "2-digit" }).format(new Date())}`;
  dom.runButton.disabled = false;
  dom.runButton.innerHTML = '<i data-lucide="rotate-cw"></i><span>Run again</span>';
  state.running = false;
  renderAll();
  showToast("Questionnaire run complete. Human review is ready.", "success");
}

function renderPipeline(stages, activeIndex) {
  dom.pipeline.innerHTML = stages
    .map(([label], index) => {
      if (index < activeIndex) {
        const value = index === 0 ? state.questions.length : index === 3 ? state.questions.filter((q) => q.flags.length).length + " flags" : state.questions.length;
        return `<li class="complete"><i data-lucide="check"></i><span>${label}</span><small>${value}</small></li>`;
      }
      if (index === activeIndex) {
        return `<li class="running"><span class="step-spinner"></span><span>${label}</span><small>Running</small></li>`;
      }
      return `<li><i data-lucide="circle"></i><span>${label}</span><small>Waiting</small></li>`;
    })
    .join("");
  refreshIcons();
}

async function exportResponses() {
  const format = dom.exportForm.querySelector('input[name="export-format"]:checked').value;
  const includeDrafts = dom.includeDrafts.checked;
  const questions = includeDrafts ? state.questions : state.questions.filter((question) => question.status === "approved");

  const backendResponse = await fetchExport(format, includeDrafts);
  if (backendResponse?._error) {
    showToast(backendResponse.detail, "warning");
    return;
  }
  if (backendResponse) {
    const blob = await backendResponse.blob();
    downloadBlob(blob, filenameFromDisposition(backendResponse.headers.get("content-disposition")) || `evidenceops-export.${format}`);
    showToast("Export downloaded", "success");
    return;
  }

  if (format === "json") {
    const body = JSON.stringify(
      {
        project: dom.projectName.textContent,
        exported_at: new Date().toISOString(),
        answers: questions,
      },
      null,
      2,
    );
    downloadBlob(new Blob([body], { type: "application/json" }), "evidenceops-responses.json");
  } else {
    const rows = questions
      .map(
        (question) => `
          <tr>
            <td>${escapeHtml(question.number)}</td><td>${escapeHtml(question.category)}</td><td>${escapeHtml(question.text)}</td>
            <td>${escapeHtml(spreadsheetSafeText(question.answer))}</td><td>${escapeHtml(STATUS_LABELS[question.status])}</td><td>${question.coverage}%</td>
            <td>${escapeHtml(question.citations.map((citation) => `${citation.source}: ${citation.location}`).join(" | "))}</td>
          </tr>`,
      )
      .join("");
    const workbook = `<html><head><meta charset="UTF-8"></head><body><table><thead><tr><th>ID</th><th>Category</th><th>Question</th><th>Answer</th><th>Status</th><th>Evidence coverage</th><th>Citations</th></tr></thead><tbody>${rows}</tbody></table></body></html>`;
    downloadBlob(new Blob([workbook], { type: "application/vnd.ms-excel" }), "evidenceops-responses.xls");
  }
  showToast(`${questions.length} responses exported`, "success");
}

async function fetchExport(format, includeDrafts) {
  if (!state.projectId) return null;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(
      `/api/projects/${encodeURIComponent(state.projectId)}/export?format=${encodeURIComponent(format)}&include_drafts=${includeDrafts}`,
      {
      method: "GET",
      signal: controller.signal,
      },
    );
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      return { _error: true, detail: payload.detail || `Export failed (${response.status})` };
    }
    return response;
  } catch (error) {
    return { _error: true, detail: error.name === "AbortError" ? "Export timed out. Please retry." : "Export request failed." };
  } finally {
    clearTimeout(timeout);
  }
}

async function apiRequest(path, options = {}) {
  const controller = new AbortController();
  const { timeoutMs = 15000, ...requestOptions } = options;
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const headers = requestOptions.body instanceof FormData ? {} : { "Content-Type": "application/json" };
    const response = await fetch(path, { ...requestOptions, headers: { ...headers, ...(requestOptions.headers || {}) }, signal: controller.signal });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      return { _error: true, status: response.status, detail: payload.detail || `Request failed (${response.status})` };
    }
    state.backendConnected = true;
    if (response.status === 204) return {};
    const contentType = response.headers.get("content-type") || "";
    return contentType.includes("application/json") ? await response.json() : {};
  } catch (error) {
    return {
      _error: true,
      status: 0,
      detail: error.name === "AbortError" ? "The request timed out. Please retry." : "The local service did not respond.",
    };
  } finally {
    clearTimeout(timeout);
  }
}

function spreadsheetSafeText(value) {
  const text = String(value ?? "");
  return /^[\s]*[=+\-@]/.test(text) ? `'${text}` : text;
}

function showToast(message, tone = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${tone}`;
  toast.innerHTML = `<i data-lucide="${tone === "success" ? "circle-check" : "triangle-alert"}"></i><span>${escapeHtml(message)}</span>`;
  dom.toastRegion.appendChild(toast);
  refreshIcons();
  window.setTimeout(() => toast.remove(), 3600);
}

function openSourceDrawer() {
  dom.sourcePanel.classList.add("open");
  dom.drawerScrim.hidden = false;
}

function closeSourceDrawer() {
  dom.sourcePanel.classList.remove("open");
  dom.drawerScrim.hidden = true;
}

function refreshIcons() {
  if (window.lucide) window.lucide.createIcons({ attrs: { "aria-hidden": "true" } });
}

function isTypingTarget(target) {
  return target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement || target?.isContentEditable;
}

function fileExtension(name) {
  const extension = String(name).split(".").pop().toLowerCase();
  if (["xlsx", "xls", "csv"].includes(extension)) return "xlsx";
  if (["doc", "docx"].includes(extension)) return "doc";
  if (extension === "pdf") return "pdf";
  if (extension === "json") return "json";
  return "txt";
}

function fileTypeLabel(type) {
  return { pdf: "PDF", doc: "DOC", xlsx: "XL", json: "{ }", txt: "TXT" }[type] || "FILE";
}

function safeClass(value) {
  return ["pdf", "doc", "xlsx", "json", "txt"].includes(value) ? value : "txt";
}

function formatBytes(bytes) {
  if (!Number.isFinite(bytes) || bytes === 0) return "0 KB";
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function filenameFromDisposition(value) {
  return value?.match(/filename="?([^";]+)"?/i)?.[1] ?? null;
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}
