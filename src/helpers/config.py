from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): # we inherit from BaseSettings
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILES_DEFAULT_CHUNK_SIZE: int
    
    MONGODB_URL: str
    MONGODB_DB_NAME: str

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()


