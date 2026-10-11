import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def get_db():
    """Yield a database session per request. FastAPI closes it automatically."""
    with Session(engine) as session:
        yield session
