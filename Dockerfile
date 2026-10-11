# Stage 1: build the React frontend
FROM node:22-alpine AS frontend

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# Stage 2: Python API that also serves the built frontend
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app
COPY --from=frontend /frontend/dist ./frontend/dist

# Run as an unprivileged user; archives are written to /app/archives (mounted as a volume).
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/archives \
    && chown -R appuser /app/archives
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
    CMD python -c "import os, sys, urllib.request; port = os.environ.get('PORT', '8000'); sys.exit(0 if urllib.request.urlopen(f'http://127.0.0.1:{port}/api/health', timeout=2).status == 200 else 1)"

# Hosting platforms such as Render choose the port via $PORT. Forwarded headers are ignored on
# purpose: Render sets FORWARDED_ALLOW_IPS=*, so uvicorn would trust any client-sent
# X-Forwarded-For. The visitor IP for the AI limit comes from CLIENT_IP_HEADER instead.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --no-proxy-headers"]
