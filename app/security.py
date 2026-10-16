from pwdlib import PasswordHash
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.database import get_db
from app.models import User
from sqlmodel import Session, select

# OAuth2-style password flow expects a login endpoint at /login/.
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

# Load secrets from environment variables, especially the JWT signing key.
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Use the recommended password hashing algorithm for secure password storage.
password_hash = PasswordHash.recommended()


def get_current_user(token: Annotated[str, Depends(oauth_scheme)], db: Annotated[Session, Depends(get_db)]) -> User:
    """Validate a JWT and return the matching user from the database."""
    # Decode and validate the bearer token sent with the request.
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    # Fetch the user by username to ensure the token owner still exists.
    user = db.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def create_token(username: str) -> str:
    """Create a signed JWT for a successfully authenticated user."""
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> str | None:
    """Check whether a JWT is valid and return the embedded username."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None


def hash_password(password: str)->str:
    """Hash a plain-text password before storing it in the database."""
    return password_hash.hash(password)


def verify_password(plain: str, hashed: str)->bool:
    """Compare a plain-text password with its hashed value."""
    return password_hash.verify(plain, hashed)