import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_NAME = os.getenv("DATABASE_NAME")

# for testing without access to .env file
if not DB_NAME:
    DB_NAME = "my_database.db"

DATABASE_URL = "sqlite:///data/" + DB_NAME


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()