from sqlmodel import Field, SQLModel


# Represents a user record in the database.
class User(SQLModel, table=True):
    # Matches the database table name used by SQLModel metadata.
    __tablename__ = "users"

    # Auto-increment primary key for each user.
    id: int | None = Field(default=None, primary_key=True)

    # Unique login name. Indexed for faster lookup during authentication.
    username: str = Field(unique=True, index=True)

    # Store only the hashed password, never the plain-text password.
    hashed_password: str
