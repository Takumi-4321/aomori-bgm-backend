from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # .env ファイルを自動で読み込む設定
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()