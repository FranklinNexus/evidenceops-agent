FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    EVIDENCEOPS_DATA_DIR=/data

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY web ./web
COPY examples ./examples

RUN python -m pip install --no-cache-dir .

RUN useradd --create-home --uid 10001 evidenceops \
    && mkdir -p /data \
    && chown -R evidenceops:evidenceops /app /data

USER evidenceops

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "evidenceops.api:app", "--host", "0.0.0.0", "--port", "8000"]
