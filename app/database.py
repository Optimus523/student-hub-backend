import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# Load environment variables from the local .env file, if present.
load_dotenv()

# Read the database connection string from the environment.
DATABASE_URL = os.getenv("DATABASE_URL")

# Build the SQLAlchemy/SQLModel engine used by all database sessions.
engine = create_engine(DATABASE_URL)


def get_db():
    """Yield a database session per request. FastAPI closes it automatically."""
    # Each request gets a separate session so database work stays isolated.
    with Session(engine) as session:
        yield session
