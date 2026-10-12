"""Application settings, read from environment variables or a local .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # SQLite works out of the box; set a PostgreSQL URL for production-like setups, e.g.
    # postgresql+psycopg://user:password@localhost:5432/medkb
    database_url: str = "sqlite:///./medkb.db"

    # Where JSON archive files are written.
    archive_dir: Path = Path("archives")

    # Insert the bundled example entries on startup if the database is empty.
    seed_demo_data: bool = False

    # Signing key for login tokens (JWT). Empty = a random key per process (logins end on restart).
    jwt_secret: str = ""
    jwt_hours: float = 8

    # Demo mode: one-click demo logins per role and a periodic reset of the example data.
    demo_mode: bool = False
    demo_reset_hours: float = 24

    # Optional password for a real "admin" login (works with and without demo mode).
    admin_password: str = ""

    # External sources (PubMed, WHO ICD-11, openFDA). An NCBI key only raises the rate limit;
    # ICD-11 needs free API keys from https://icd.who.int/icdapi.
    ncbi_api_key: str = ""
    icd_client_id: str = ""
    icd_client_secret: str = ""
    icd_release: str = "2026-01"
    icd_language: str = "de"
    sources_timeout: float = 8
    source_cache_hours: float = 24

    # Optional OpenAI-compatible AI provider. No key means clearly disabled features.
    ai_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    ai_api_key: str = ""
    ai_model: str = "gemini-3.5-flash-lite"
    ai_timeout: float = Field(default=30, gt=0, le=120)
    ai_daily_limit: int = Field(default=500, ge=1)
    ai_client_daily_limit: int = Field(default=30, ge=1)
    # Semantic retrieval is opt-in until its persisted index and real evaluation are ready.
    rag_enabled: bool = False
    embedding_api_key: str = ""
    embedding_timeout: float = Field(default=15, gt=0, le=120)
    rag_min_similarity: float = Field(default=0.45, ge=0, le=1)
    rag_max_chunks: int = Field(default=5000, ge=1, le=5000)
    # Behind a reverse proxy: the request header that carries the visitor's IP, set by the
    # proxy itself (e.g. True-Client-IP on Render). Empty = the connection's address. Only set
    # it when the proxy overwrites the header, otherwise visitors could reset their quota.
    client_ip_header: str = ""

    # Built React frontend (npm run build). Missing directory = API only, with a hint page at /.
    frontend_dist: Path = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@lru_cache
def get_settings() -> Settings:
    return Settings()
