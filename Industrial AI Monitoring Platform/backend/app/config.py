from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://industrial:industrial@postgres:5432/industrial_ai"
    )

    model_path: str = "/app/ml/model.joblib"

    class Config:
        env_file = ".env"


settings = Settings()