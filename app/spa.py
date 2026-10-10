"""Serve the built React frontend (frontend/dist); unknown paths fall back to index.html."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
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
        # Hashed file names: safe to cache for a long time.
        app.mount("/assets", StaticFiles(directory=dist_dir / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend(full_path: str) -> FileResponse:
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")
        if full_path:
            candidate = (root / full_path).resolve()
            if candidate.is_file() and root in candidate.parents:
                return FileResponse(candidate)
        # Client-side route: the React router decides. Never cache the shell.
        return FileResponse(index, headers={"Cache-Control": "no-cache"})
