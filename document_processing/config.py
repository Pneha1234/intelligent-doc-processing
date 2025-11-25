"""
Configuration helpers for loading environment variables and shared settings.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

# Load .env if present; fall back to shell environment otherwise.
load_dotenv(ENV_PATH)


@dataclass(frozen=True)
class Settings:
    """Runtime configuration settings."""

    google_api_key: str
    google_model: str = "gemini-1.5-flash"
    use_vertex_ai: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        """Construct settings from the environment."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is not set. Please add it to your environment or .env file."
            )

        use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"
        model = os.getenv("GOOGLE_GENAI_MODEL", "gemini-1.5-flash")

        # Ensure ADK downstream gets consistent configuration.
        os.environ["GOOGLE_API_KEY"] = api_key
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE" if use_vertex else "FALSE"
        os.environ["GOOGLE_GENAI_MODEL"] = model

        return cls(
            google_api_key=api_key,
            google_model=model,
            use_vertex_ai=use_vertex,
        )


settings = Settings.from_env()

