import os

from dotenv import load_dotenv
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
localsession=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=localsession()
    try:
        yield db
    finally:
        db.close()