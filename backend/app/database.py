import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.tickets.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./support.db")
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
