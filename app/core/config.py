from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    DB_MODE: str = "container" # local, container
    MONGODB_DOCKER_HOST: str = "mongodb"
    MONGODB_LOCAL_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "test_database"
    
    SECRET_KEY: str = "CHANGE THIS IN PRODUCTION"
    ALGORITHM: str = "HS256"
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    AUTH_SERVICE_TOKEN_URL: str = f"{AUTH_SERVICE_URL}/api/v1/login/access-token"
    
    # for testing
    EXPENSE_TRACKER_URL: str = "http://127.0.0.1:8000"
    TEST_DB_NAME: str = MONGODB_DB_NAME + "_test"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
