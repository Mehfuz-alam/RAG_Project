from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    pinecone_api_key: str
    pinecone_index_name: str

    gemini_api_key: str

    redis_host: str
    db_url: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()