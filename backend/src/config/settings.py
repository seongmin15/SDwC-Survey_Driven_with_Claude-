from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_URL: str = "postgresql+psycopg://sdwc:sdwc@localhost:5432/sdwc"

    model_config = {"env_file": ".env", "extra": "ignore"}


def get_settings() -> Settings:
    return Settings()
