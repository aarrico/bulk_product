from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Bulk Product"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bulk_product"

    # CORS — React dev server
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
