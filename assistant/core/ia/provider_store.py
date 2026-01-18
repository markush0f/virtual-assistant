"""
SQLite-backed storage for AI provider configuration.
Keeps a single row with provider type, model name, and optional API key.
"""

import sqlite3
from pathlib import Path
from typing import Optional, Literal

# Database path lives under assistant/common
DB_PATH = Path(__file__).parent.parent / "common" / "settings.db"

# Allowed providers
ProviderType = Literal["local", "openai"]


def _ensure_db():
    """Create the provider_config table and default row if missing."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS provider_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                api_key TEXT
            )
            """
        )
        cur = conn.execute("SELECT COUNT(*) FROM provider_config WHERE id = 1")
        exists = cur.fetchone()[0]
        if not exists:
            conn.execute(
                "INSERT INTO provider_config (id, provider, model, api_key) VALUES (1, ?, ?, ?)",
                ("local", "mistral:7b-instruct", None),
            )
        conn.commit()


def get_provider_config() -> dict:
    """Return the current provider configuration."""
    _ensure_db()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT provider, model, api_key FROM provider_config WHERE id = 1"
        )
        row = cur.fetchone()
        if not row:
            return {"provider": "local", "model": "mistral:7b-instruct", "api_key": None}
        provider, model, api_key = row
        return {"provider": provider, "model": model, "api_key": api_key}


def set_provider_config(provider: ProviderType, model: str, api_key: Optional[str] = None):
    """
    Persist provider configuration.
    provider: "local" or "openai"
    model: model id for the chosen provider (e.g., "mistral:7b-instruct" or "gpt-4o-mini")
    api_key: required for OpenAI provider
    """
    _ensure_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO provider_config (id, provider, model, api_key)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET provider=excluded.provider, model=excluded.model, api_key=excluded.api_key
            """,
            (provider, model, api_key),
        )
        conn.commit()
