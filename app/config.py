"""Application settings, read from environment variables or a local .env file."""

from functools import lru_cache
from pathlib import Path

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

    # Built React frontend (npm run build). Missing directory = API only, with a hint page at /.
    frontend_dist: Path = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@lru_cache
def get_settings() -> Settings:
    return Settings()
