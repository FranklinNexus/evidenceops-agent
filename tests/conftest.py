from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from evidenceops.api import create_app
from evidenceops.config import Settings


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    settings = Settings(data_dir=tmp_path, provider="demo")
    with TestClient(create_app(settings)) as test_client:
        yield test_client
