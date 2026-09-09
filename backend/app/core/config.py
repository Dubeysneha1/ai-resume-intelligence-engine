from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer"
    API_V1_STR: str = "/api/v1"

    # File handling constraints
    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: set[str] = {"pdf"}

    # API Keys
    GROK_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Prevents crashing if extra env vars exist
    )


settings = Settings()