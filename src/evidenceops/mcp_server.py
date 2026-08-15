from __future__ import annotations

from typing import Any

from .api import create_app
from .models import VerifyEvidenceRequest


def build_mcp_server() -> Any:
    """Optional thin MCP transport over the same service boundary used by FastAPI."""
    from mcp.server.fastmcp import FastMCP

    application = create_app()
    service = application.state.service
    server = FastMCP("EvidenceOps")

    @server.tool()
    def verify_evidence(
        tenant_id: str,
        question: str,
        answer: str,
        citations: list[dict[str, str]],
        project_id: str | None = None,
    ) -> dict[str, Any]:
        """Verify that an answer is grounded in exact document/location/quote citations."""
        result = service.verify_evidence(
            VerifyEvidenceRequest(
                tenant_id=tenant_id,
                question=question,
                answer=answer,
                citations=citations,
                project_id=project_id,
            )
        )
        return result.model_dump()

    return server


def main() -> None:
    build_mcp_server().run()


if __name__ == "__main__":
    main()
