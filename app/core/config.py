from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "test_database"
    
    SECRET_KEY: str = "CHANGE THIS IN PRODUCTION"
    ALGORITHM: str = "HS256"
    AUTH_SERVICE_URL: str = "http://127.0.0.1:5000"
    AUTH_SERVICE_TOKEN_URL: str = f"{AUTH_SERVICE_URL}/api/v1/login/access-token"
    
    MOCK_TOKEN: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM4NjQwMzksInN1YiI6ImFhOTA5MjFmLWQ2YjktNDhkOC05M2M2LWZjYTg5M2ZjMGNiMCJ9.Hl6cd7KsH-gGrjVZsjE0txs26qm6jsMzMrUfh0lQwpI"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
