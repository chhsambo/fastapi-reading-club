from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Field name matches env var exactly

settings = Settings()
