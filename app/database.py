from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLACHEMY_DB_URL = f"postgresql://{settings.pguser}:{settings.pgpass}@{settings.pghost}:{settings.pgport}/{settings.pg_db_name}"
engine = create_engine(SQLACHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()