from __future__ import annotations

import asyncio
from pathlib import Path

from evidenceops.mcp_server import build_mcp_server
from evidenceops.models import DocumentKind
from evidenceops.retrieval import retrieve
from evidenceops.store import SQLiteStore


def test_mcp_verify_accepts_full_api_citation(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("EVIDENCEOPS_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EVIDENCEOPS_PROVIDER", "demo")
    store = SQLiteStore(tmp_path)
    project = store.create_project("MCP contract", tenant_id="tenant-mcp")
    store.add_document(
        project.id,
        "policy.txt",
        DocumentKind.evidence,
        "text/plain",
        [{"text": "Backups are retained for 30 days.", "page_or_sheet": "Line 1"}],
    )
    citation = retrieve("How long are backups retained?", store.list_chunks(project.id))[0]
    server = build_mcp_server()

    result = asyncio.run(
        server.call_tool(
            "verify_evidence",
            {
                "tenant_id": "tenant-mcp",
                "project_id": project.id,
                "question": "How long are backups retained?",
                "answer": "Backups are retained for 30 days.",
                "citations": [citation.model_dump()],
            },
        )
    )

    _, structured = result
    assert structured["grounded"] is True
    assert structured["citation_integrity"][0]["verified"] is True
