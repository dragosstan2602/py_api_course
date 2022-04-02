from pydantic import BaseSettings

# Used to grab the env vars - case insensitive
class Settings(BaseSettings):
    pgpass: str
    pguser: str
    oauth2_secret_key: str
    oauth2_alg: str
    pghost: str
    pgport: str
    pg_db_name: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"

settings = Settings()