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


    CELERY_BROKER_URL: str 
    CELERY_RESULT_BACKEND: str 
    CELERY_TASK_SERIALIZER: str 
    CELERY_TASK_TIME_LIMIT: int
    CELERY_TASK_ACKS_LATE : bool 
    CELERY_WORKER_CONCURRENCY: int
    CELERY_FLOWER_PASSWORD : str

    class Config:
        env_file = ".env"



def get_settings():
    return Settings()