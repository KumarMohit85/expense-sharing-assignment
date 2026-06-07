from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()