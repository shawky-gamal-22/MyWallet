from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    PATH_TO_OCR_ENGINE: str

    MISTRAL_API_KEY: str
    GROQ_API_KEY: str
    GENERATION_MODEL_ID: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int
    POSTGRES_MAIN_DATABASE: str

    class Config:
        env_file = ".env"



def get_settings():
    return Settings()