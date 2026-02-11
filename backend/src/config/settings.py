from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_URL: str = "postgresql+psycopg://sdwc:sdwc@localhost:5432/sdwc"
    OUTPUT_DIR: str = "./generated_output"

    model_config = {"env_file": ".env", "extra": "ignore"}


def get_settings() -> Settings:
    return Settings()
