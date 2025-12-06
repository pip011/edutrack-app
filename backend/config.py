from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = 'bcd0f523d3d5f04bcf942bb8eec4371b'
    
    class Config:
        env_file = '.env'
        
        
settings = Settings()