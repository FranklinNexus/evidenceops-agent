from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from .models import (
    Citation,
    DocumentKind,
    DocumentRecord,
    EvidenceChecks,
    Project,
    QuestionRecord,
    ReviewStatus,
    StoredChunk,
    utc_now,
)


class NotFoundError(LookupError):
    pass


class SQLiteStore:
    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        self.path = data_dir / "evidenceops.sqlite3"
        self._lock = threading.RLock()
        self._initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL DEFAULT 'demo', name TEXT NOT NULL,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    filename TEXT NOT NULL, kind TEXT NOT NULL, content_type TEXT, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY, document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    text TEXT NOT NULL, page_or_sheet TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS questions (
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    question TEXT NOT NULL, source_document TEXT, source_locator TEXT, status TEXT NOT NULL,
                    answer TEXT, citations_json TEXT NOT NULL, checks_json TEXT, missing_evidence TEXT,
                    provider TEXT, reviewer_note TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_documents_project ON documents(project_id);
                CREATE INDEX IF NOT EXISTS idx_chunks_project ON chunks(project_id);
                CREATE INDEX IF NOT EXISTS idx_questions_project ON questions(project_id);
                CREATE TABLE IF NOT EXISTS tool_audit (
                    id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, request_id TEXT NOT NULL,
                    action TEXT NOT NULL, request_hash TEXT NOT NULL, cached INTEGER NOT NULL,
                    outcome TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_tool_audit_tenant_created
                    ON tool_audit(tenant_id, created_at);
                """
            )

            project_columns = {row[1] for row in connection.execute("PRAGMA table_info(projects)")}
            if "tenant_id" not in project_columns:
                connection.execute("ALTER TABLE projects ADD COLUMN tenant_id TEXT NOT NULL DEFAULT 'demo'")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_projects_tenant ON projects(tenant_id)")

    def create_project(self, name: str, tenant_id: str = "demo") -> Project:
        project_id = uuid.uuid4().hex
        now = utc_now()
        with self._lock, self._connect() as connection:
            connection.execute(
                "INSERT INTO projects (id, tenant_id, name, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (project_id, tenant_id, name.strip(), now, now),
            )
        return Project(id=project_id, tenant_id=tenant_id, name=name.strip(), created_at=now, updated_at=now)

    def _require_project(self, connection: sqlite3.Connection, project_id: str) -> sqlite3.Row:
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"Project {project_id} not found")
        return row

    def get_project(self, project_id: str) -> Project:
        with self._connect() as connection:
            row = self._require_project(connection, project_id)
            document_count = connection.execute(
                "SELECT COUNT(*) FROM documents WHERE project_id = ?", (project_id,)
            ).fetchone()[0]
            question_count = connection.execute(
                "SELECT COUNT(*) FROM questions WHERE project_id = ?", (project_id,)
            ).fetchone()[0]
        return Project(**dict(row), document_count=document_count, question_count=question_count)

    def list_projects(self) -> list[Project]:
        with self._connect() as connection:
            ids = [row[0] for row in connection.execute("SELECT id FROM projects ORDER BY created_at DESC")]
        return [self.get_project(project_id) for project_id in ids]

    def project_belongs_to(self, project_id: str, tenant_id: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM projects WHERE id = ? AND tenant_id = ?", (project_id, tenant_id)
            ).fetchone()
        return row is not None

    def record_tool_audit(
        self,
        *,
        tenant_id: str,
        request_id: str,
        action: str,
        request_hash: str,
        cached: bool,
        outcome: str,
    ) -> str:
        audit_id = uuid.uuid4().hex
        with self._lock, self._connect() as connection:
            connection.execute(
                """INSERT INTO tool_audit
                   (id, tenant_id, request_id, action, request_hash, cached, outcome, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (audit_id, tenant_id, request_id, action, request_hash, int(cached), outcome, utc_now()),
            )
        return audit_id

    def add_document(
        self,
        project_id: str,
        filename: str,
        kind: DocumentKind,
        content_type: str | None,
        chunks: list[dict[str, str]],
    ) -> DocumentRecord:
        document_id = uuid.uuid4().hex
        now = utc_now()
        with self._lock, self._connect() as connection:
            self._require_project(connection, project_id)
            connection.execute(
                "INSERT INTO documents (id, project_id, filename, kind, content_type, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (document_id, project_id, filename, kind.value, content_type, now),
            )
            connection.executemany(
                "INSERT INTO chunks (id, document_id, project_id, text, page_or_sheet) VALUES (?, ?, ?, ?, ?)",
                [
                    (uuid.uuid4().hex, document_id, project_id, chunk["text"], chunk["page_or_sheet"])
                    for chunk in chunks
                ],
            )
            connection.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now, project_id))
        return DocumentRecord(
            id=document_id,
            project_id=project_id,
            filename=filename,
            kind=kind,
            content_type=content_type,
            chunk_count=len(chunks),
            created_at=now,
        )

    def list_documents(self, project_id: str) -> list[DocumentRecord]:
        with self._connect() as connection:
            self._require_project(connection, project_id)
            rows = connection.execute(
                """SELECT d.*, COUNT(c.id) AS chunk_count FROM documents d
                   LEFT JOIN chunks c ON c.document_id = d.id WHERE d.project_id = ?
                   GROUP BY d.id ORDER BY d.created_at""",
                (project_id,),
            ).fetchall()
        return [DocumentRecord(**dict(row)) for row in rows]

    def list_chunks(self, project_id: str, kind: DocumentKind = DocumentKind.evidence) -> list[StoredChunk]:
        with self._connect() as connection:
            self._require_project(connection, project_id)
            rows = connection.execute(
                """SELECT c.id, c.document_id, d.filename AS document, c.text, c.page_or_sheet
                   FROM chunks c JOIN documents d ON d.id = c.document_id
                   WHERE c.project_id = ? AND d.kind = ? ORDER BY d.created_at, c.rowid""",
                (project_id, kind.value),
            ).fetchall()
        return [StoredChunk(**dict(row)) for row in rows]

    def add_questions(
        self,
        project_id: str,
        questions: list[str],
        *,
        source_document: str | None = None,
        source_locators: list[str | None] | None = None,
    ) -> list[QuestionRecord]:
        now = utc_now()
        records: list[QuestionRecord] = []
        locators = source_locators or [None] * len(questions)
        with self._lock, self._connect() as connection:
            self._require_project(connection, project_id)
            existing = {
                row[0].casefold()
                for row in connection.execute("SELECT question FROM questions WHERE project_id = ?", (project_id,))
            }
            for question, locator in zip(questions, locators, strict=False):
                cleaned = question.strip()
                if not cleaned or cleaned.casefold() in existing:
                    continue
                question_id = uuid.uuid4().hex
                connection.execute(
                    """INSERT INTO questions
                       (id, project_id, question, source_document, source_locator, status, answer, citations_json,
                        checks_json, missing_evidence, provider, reviewer_note, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, NULL, '[]', NULL, NULL, NULL, NULL, ?, ?)""",
                    (
                        question_id, project_id, cleaned, source_document, locator, ReviewStatus.pending.value, now, now
                    ),
                )
                records.append(
                    QuestionRecord(
                        id=question_id,
                        project_id=project_id,
                        question=cleaned,
                        source_document=source_document,
                        source_locator=locator,
                        created_at=now,
                        updated_at=now,
                    )
                )
                existing.add(cleaned.casefold())
            connection.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now, project_id))
        return records

    @staticmethod
    def _question_from_row(row: sqlite3.Row) -> QuestionRecord:
        data = dict(row)
        data["citations"] = [Citation.model_validate(item) for item in json.loads(data.pop("citations_json"))]
        checks = data.pop("checks_json")
        data["checks"] = EvidenceChecks.model_validate(json.loads(checks)) if checks else None
        return QuestionRecord(**data)

    def list_questions(self, project_id: str) -> list[QuestionRecord]:
        with self._connect() as connection:
            self._require_project(connection, project_id)
            rows = connection.execute(
                "SELECT * FROM questions WHERE project_id = ? ORDER BY created_at, rowid", (project_id,)
            ).fetchall()
        return [self._question_from_row(row) for row in rows]

    def get_question(self, project_id: str, question_id: str) -> QuestionRecord:
        with self._connect() as connection:
            self._require_project(connection, project_id)
            row = connection.execute(
                "SELECT * FROM questions WHERE project_id = ? AND id = ?", (project_id, question_id)
            ).fetchone()
        if row is None:
            raise NotFoundError(f"Question {question_id} not found")
        return self._question_from_row(row)

    def update_question(self, project_id: str, question_id: str, **updates: Any) -> QuestionRecord:
        allowed = {
            "status", "answer", "citations_json", "checks_json", "missing_evidence", "provider", "reviewer_note"
        }
        invalid = set(updates) - allowed
        if invalid:
            raise ValueError(f"Unsupported question fields: {sorted(invalid)}")
        now = utc_now()
        values = dict(updates)
        values["updated_at"] = now
        assignment = ", ".join(f"{field} = ?" for field in values)
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                f"UPDATE questions SET {assignment} WHERE project_id = ? AND id = ?",
                (*values.values(), project_id, question_id),
            )
            if cursor.rowcount == 0:
                raise NotFoundError(f"Question {question_id} not found")
            connection.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now, project_id))
        return self.get_question(project_id, question_id)

    def find_quote(self, project_id: str, citation: Citation) -> bool:
        with self._connect() as connection:
            self._require_project(connection, project_id)
            if citation.chunk_id:
                row = connection.execute(
                    """SELECT c.text, c.page_or_sheet, d.filename FROM chunks c JOIN documents d ON d.id = c.document_id
                       WHERE c.project_id = ? AND c.id = ?""",
                    (project_id, citation.chunk_id),
                ).fetchone()
                if row:
                    return (
                        citation.quote in row["text"]
                        and citation.document == row["filename"]
                        and citation.page_or_sheet == row["page_or_sheet"]
                    )
            rows = connection.execute(
                """SELECT c.text FROM chunks c JOIN documents d ON d.id = c.document_id
                   WHERE c.project_id = ? AND d.filename = ? AND c.page_or_sheet = ?""",
                (project_id, citation.document, citation.page_or_sheet),
            ).fetchall()
        return any(citation.quote in row["text"] for row in rows)
