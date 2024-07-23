from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # default if not specified in env file
    MONGO_DB_URL: str = "mongodb://localhost:27017/"
    MONGO_DB: str
    MONGO_COLLECTION: str
    # default if not specified in env file
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env")


# global instance
settings = Settings()
