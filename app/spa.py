"""Serve the built React frontend (frontend/dist); unknown paths fall back to index.html."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

NOT_BUILT_PAGE = """<!doctype html>
<html lang="de"><meta charset="utf-8"><title>MedKB</title>
<body style="font-family: system-ui, sans-serif; max-width: 40rem; margin: 4rem auto">
<h1>Frontend nicht gebaut</h1>
<p>Die API läuft unter <a href="/docs">/docs</a>. Für die Oberfläche einmal bauen:</p>
<pre>cd frontend &amp;&amp; npm install &amp;&amp; npm run build</pre>
<p>Oder im Entwicklungsmodus <code>npm run dev</code> starten und
<a href="http://localhost:5173">localhost:5173</a> öffnen.</p>
</body></html>"""


SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
}
ASSET_CACHE = "public, max-age=31536000, immutable"


class HashedAssets(StaticFiles):
    """Vite puts a content hash in every asset name, so a cached copy can never be stale."""

    def file_response(self, *args: Any, **kwargs: Any):
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = ASSET_CACHE
        return response


def install_security_headers(app: FastAPI) -> None:
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        for name, value in SECURITY_HEADERS.items():
            response.headers.setdefault(name, value)
        return response


def mount_frontend(app: FastAPI, dist_dir: Path) -> None:
    """Register routes for the single-page app. Call after all API routers are included."""
    index = dist_dir / "index.html"

    if not index.is_file():

        @app.get("/", include_in_schema=False)
        def frontend_missing() -> HTMLResponse:
            return HTMLResponse(NOT_BUILT_PAGE)

        return

    root = dist_dir.resolve()
    if (dist_dir / "assets").is_dir():
        app.mount("/assets", HashedAssets(directory=dist_dir / "assets"), name="assets")

    @app.api_route("/{full_path:path}", methods=["GET", "HEAD"], include_in_schema=False)
    def frontend(full_path: str) -> FileResponse:
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")
        if full_path:
            candidate = (root / full_path).resolve()
            if candidate == index.resolve():
                return FileResponse(index, headers={"Cache-Control": "no-cache"})
            if candidate.is_file() and root in candidate.parents:
                return FileResponse(candidate)
        # Client-side route: the React router decides. Never cache the shell.
        return FileResponse(index, headers={"Cache-Control": "no-cache"})
