from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "professional-rag-platform"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "postgresql://postgres:postgres@localhost:5432/rag_db"

    llm_provider: str = ""
    llm_model: str = ""
    openai_api_key: str = ""

    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    vector_store: str = "pgvector"

    top_k: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
