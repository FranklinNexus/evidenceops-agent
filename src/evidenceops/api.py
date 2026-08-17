from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

from fastapi import APIRouter, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from .config import Settings
from .demo import demo_files
from .models import (
    AddQuestionsRequest,
    CreateProjectRequest,
    DocumentKind,
    ProviderInfo,
    ReviewRequest,
    SaveDraftRequest,
    VerifyEvidenceRequest,
    VerifyEvidenceResponse,
)
from .parsers import DocumentParseError, UnsupportedDocumentError
from .providers import ResilientProvider, build_provider
from .service import EvidenceOpsService, TenantRateLimitExceeded
from .store import NotFoundError, SQLiteStore


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    store = SQLiteStore(settings.data_dir)
    provider = build_provider(settings)
    service = EvidenceOpsService(store, provider, settings)
    application = FastAPI(
        title="EvidenceOps API",
        version="0.1.0",
        description="Evidence-grounded compliance and RFP questionnaire workflow",
    )
    application.state.service = service
    application.state.settings = settings
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    router = APIRouter(prefix="/api")

    def get_service(request: Request) -> EvidenceOpsService:
        return request.app.state.service

    @application.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> Response:
        return JSONResponse(content={"detail": str(exc)}, status_code=404)

    @application.exception_handler(TenantRateLimitExceeded)
    async def tenant_rate_limit_handler(_: Request, exc: TenantRateLimitExceeded) -> Response:
        return JSONResponse(content={"detail": str(exc)}, status_code=429)

    @router.get("/health")
    def health(request: Request) -> dict[str, object]:
        current_provider = get_service(request).provider
        circuit_state = current_provider.circuit_state if isinstance(current_provider, ResilientProvider) else "closed"
        provider_info = ProviderInfo(
            configured=settings.provider,
            active=current_provider.name,
            circuit_state=circuit_state,
        )
        return {"status": "ok", "version": "0.1.0", "provider": provider_info.model_dump()}

    @router.post("/projects", status_code=201)
    def create_project(payload: CreateProjectRequest, request: Request):
        return get_service(request).store.create_project(payload.name, payload.tenant_id)

    @router.get("/projects")
    def list_projects(request: Request):
        return get_service(request).store.list_projects()

    @router.post("/demo", status_code=201)
    def create_synthetic_demo(request: Request):
        service = get_service(request)
        try:
            questionnaire, evidence_files = demo_files()
        except FileNotFoundError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        project = service.store.create_project("CloudDesk Synthetic Review")
        service.upload_document(
            project.id,
            filename=questionnaire[0],
            data=questionnaire[1],
            kind=DocumentKind.questionnaire,
            content_type="text/csv",
        )
        for filename, data in evidence_files:
            service.upload_document(
                project.id,
                filename=filename,
                data=data,
                kind=DocumentKind.evidence,
                content_type="text/markdown",
            )
        return {
            "project": project,
            "documents": service.store.list_documents(project.id),
            "questions": service.store.list_questions(project.id),
        }

    @router.get("/projects/{project_id}")
    def get_project(project_id: str, request: Request):
        service = get_service(request)
        return {
            "project": service.store.get_project(project_id),
            "documents": service.store.list_documents(project_id),
            "questions": service.store.list_questions(project_id),
        }

    @router.post("/projects/{project_id}/documents", status_code=201)
    async def upload_documents(
        project_id: str,
        request: Request,
        files: Annotated[list[UploadFile], File(description="PDF, XLSX, DOCX, TXT, MD, or CSV files")],
        kind: Annotated[DocumentKind, Query()] = DocumentKind.evidence,
    ):
        service = get_service(request)
        results = []
        for upload in files:
            try:
                data = await upload.read(service.settings.max_upload_mb * 1024 * 1024 + 1)
                result = service.upload_document(
                    project_id,
                    filename=upload.filename or "upload",
                    data=data,
                    kind=kind,
                    content_type=upload.content_type,
                )
            except (UnsupportedDocumentError, DocumentParseError, ValueError) as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc
            results.append(
                {"document": result.document, "questions_added": result.questions_added}
            )
        return {"uploads": results}

    @router.post("/projects/{project_id}/upload", status_code=201, include_in_schema=False)
    async def upload_alias(
        project_id: str,
        request: Request,
        files: Annotated[list[UploadFile], File()],
        kind: Annotated[DocumentKind, Query()] = DocumentKind.evidence,
    ):
        return await upload_documents(project_id, request, files, kind)

    @router.post("/projects/{project_id}/questions", status_code=201)
    def add_questions(project_id: str, payload: AddQuestionsRequest, request: Request):
        return {
            "questions": get_service(request).add_manual_questions(project_id, payload.questions, payload.text)
        }

    @router.get("/projects/{project_id}/questions")
    def list_questions(project_id: str, request: Request):
        return get_service(request).store.list_questions(project_id)

    @router.post("/projects/{project_id}/run")
    def run_project(project_id: str, request: Request):
        return get_service(request).run_project(project_id)

    @router.patch("/projects/{project_id}/questions/{question_id}/review")
    def review_question(project_id: str, question_id: str, payload: ReviewRequest, request: Request):
        try:
            return get_service(request).review_question(project_id, question_id, payload)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @router.patch("/projects/{project_id}/questions/{question_id}")
    def save_draft(project_id: str, question_id: str, payload: SaveDraftRequest, request: Request):
        return get_service(request).save_draft(project_id, question_id, payload)

    @router.get("/projects/{project_id}/missing-evidence")
    def missing_evidence(project_id: str, request: Request):
        questions = get_service(request).store.list_questions(project_id)
        return {
            "items": [
                {"question_id": question.id, "question": question.question, "needed": question.missing_evidence}
                for question in questions
                if question.missing_evidence
            ]
        }

    @router.get("/projects/{project_id}/export")
    def export_project(
        project_id: str,
        request: Request,
        format: Literal["csv", "json", "xlsx"] = Query(default="xlsx"),
        include_drafts: bool = Query(default=False),
    ) -> Response:
        body, media_type, filename = get_service(request).export_project(
            project_id, format, include_drafts=include_drafts
        )
        return Response(
            content=body,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    @router.post("/tools/verify-evidence", response_model=VerifyEvidenceResponse)
    def verify_evidence(payload: VerifyEvidenceRequest, request: Request):
        return get_service(request).verify_evidence(payload)

    application.include_router(router)

    web_dir = Path("web").resolve()
    if not web_dir.is_dir():
        web_dir = Path(__file__).resolve().parent / "web"
    if web_dir.is_dir():
        application.mount("/web", StaticFiles(directory=web_dir), name="web")

        @application.get("/", include_in_schema=False)
        def workspace() -> FileResponse:
            return FileResponse(web_dir / "index.html")

    return application


app = create_app()
