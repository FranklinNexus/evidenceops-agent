from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class DocumentKind(str, Enum):
    evidence = "evidence"
    questionnaire = "questionnaire"


class ReviewStatus(str, Enum):
    pending = "pending"
    draft = "draft"
    needs_evidence = "needs_evidence"
    approved = "approved"
    rejected = "rejected"


class ParsedChunk(BaseModel):
    text: str
    page_or_sheet: str


class StoredChunk(ParsedChunk):
    id: str
    document_id: str
    document: str


class Citation(BaseModel):
    document: str
    page_or_sheet: str
    quote: str
    document_id: str | None = None
    chunk_id: str | None = None
    relevance_score: float = Field(default=0.0, ge=0.0)


class Contradiction(BaseModel):
    summary: str
    citation_indexes: list[int] = Field(default_factory=list)


class EvidenceChecks(BaseModel):
    grounded: bool
    hallucination_risk: bool
    unsupported_claims: list[str] = Field(default_factory=list)
    contradictions: list[Contradiction] = Field(default_factory=list)


class Project(BaseModel):
    id: str
    tenant_id: str = "demo"
    name: str
    created_at: str
    updated_at: str
    document_count: int = 0
    question_count: int = 0


class DocumentRecord(BaseModel):
    id: str
    project_id: str
    filename: str
    kind: DocumentKind
    content_type: str | None = None
    chunk_count: int = 0
    created_at: str


class QuestionRecord(BaseModel):
    id: str
    project_id: str
    question: str
    source_document: str | None = None
    source_locator: str | None = None
    status: ReviewStatus = ReviewStatus.pending
    answer: str | None = None
    citations: list[Citation] = Field(default_factory=list)
    checks: EvidenceChecks | None = None
    missing_evidence: str | None = None
    provider: str | None = None
    reviewer_note: str | None = None
    created_at: str
    updated_at: str


class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    tenant_id: str = Field(default="demo", min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")


class AddQuestionsRequest(BaseModel):
    questions: list[str] = Field(default_factory=list, max_length=500)
    text: str | None = Field(default=None, max_length=200_000)

    @model_validator(mode="after")
    def require_content(self) -> "AddQuestionsRequest":
        if not self.questions and not (self.text and self.text.strip()):
            raise ValueError("Provide at least one question or questionnaire text")
        return self


class ReviewRequest(BaseModel):
    action: Literal["approve", "reject"]
    edited_answer: str | None = Field(default=None, max_length=20_000)
    note: str | None = Field(default=None, max_length=2_000)


class SaveDraftRequest(BaseModel):
    edited_answer: str | None = Field(default=None, max_length=20_000)
    note: str | None = Field(default=None, max_length=2_000)


class CitationInput(BaseModel):
    document: str
    page_or_sheet: str
    quote: str = Field(min_length=1, max_length=10_000)
    document_id: str | None = None
    chunk_id: str | None = None


class VerifyEvidenceRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    request_id: str | None = Field(default=None, min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=10_000)
    answer: str = Field(min_length=1, max_length=20_000)
    citations: list[CitationInput] = Field(min_length=1, max_length=20)
    project_id: str | None = None


class CitationIntegrity(BaseModel):
    citation_index: int
    verified: bool
    reason: str


class VerifyEvidenceResponse(BaseModel):
    tenant_id: str
    request_id: str
    cached: bool = False
    grounded: bool
    hallucination_risk: bool
    unsupported_claims: list[str]
    contradictions: list[Contradiction]
    citation_integrity: list[CitationIntegrity]


class RunResponse(BaseModel):
    processed: int
    draft_count: int
    needs_evidence_count: int
    questions: list[QuestionRecord]


class ProviderInfo(BaseModel):
    configured: str
    active: str
    fallback: str = "deterministic-demo"
    circuit_state: str = "closed"
