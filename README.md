# Student Hub Backend

This repository contains the backend API for the Student Hub project, a student-focused platform for academic, administrative, and social features.

The current implementation is a FastAPI service built with SQLModel and PostgreSQL. It already supports user registration, JWT-based login, and authenticated announcement management.

## Current features

- User registration
- Username uniqueness checks
- Password hashing with Argon2
- JWT login and token validation
- Protected announcement creation and deletion routes
- Announcement listing and retrieval
- Automatic SQLModel table creation on startup
- CORS support for local frontend testing

## Tech stack

- Python 3.10+
- FastAPI
- SQLModel
- PostgreSQL
- psycopg
- python-dotenv
- pwdlib[argon2]
- PyJWT

## Project structure

```text
backend_student_hub/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── announcement.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── announcements.py
│   │   └── auth.py
│   └── schemas/
│       ├── __init__.py
│       ├── announcement.py
│       └── user.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── venv/   # local environment, excluded from Git
```

## Environment setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd backend_student_hub
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

Make sure PostgreSQL is installed and running locally, then create a database:

```sql
CREATE DATABASE student_hub;
```

### 5. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.example .env
```

Your `.env` file should look like this:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/student_hub
SECRET_KEY=your-secret-key-here
```

Notes:

- Do not commit `.env`
- Do not commit `venv/`
- Keep `SECRET_KEY` private and unique

## Run the app

You can start the server with either of these:

```bash
fastapi dev app/main.py
```

or:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API overview

### Auth routes

#### Register a user

```http
POST /users/
```

Request body:

```json
{
    "username": "edwin",
    "password": "secret123"
}
```

Behavior:

- username must be 3-30 characters
- allowed characters: letters, digits, underscores
- password must be 8-128 characters
- duplicate usernames return `409 Conflict`

#### Login

```http
POST /login/
```

Uses OAuth2 form data:

```text
username=edwin&password=secret123
```

Response:

```json
{
    "access_token": "<jwt>",
    "token_type": "bearer"
}
```

### Announcements routes

#### Create an announcement

```http
POST /announcements/
```

Requires a valid JWT in the Authorization header.

Example request body:

```json
{
    "title": "Exam timetable",
    "body": "The timetable is now available on the notice board."
}
```

#### List announcements

```http
GET /announcements/
```

#### Get one announcement

```http
GET /announcements/{id}
```

#### Delete an announcement

```http
DELETE /announcements/{id}
```

Requires authentication.

## Authentication and security

This backend uses JWT-based authentication:

- `POST /login/` issues a signed token
- `get_current_user()` validates the token
- protected routes require a bearer token in the `Authorization` header
- passwords are never stored in plain text
- Argon2 is used for password hashing

Example:

```http
Authorization: Bearer <your-token>
```

## Database model summary

### User

- `id`: primary key
- `username`: unique username
- `hashed_password`: secure Argon2 hash

### Announcement

- `id`: primary key
- `title`: announcement headline
- `body`: message content
- `author_id`: foreign key to the user who created it

## Notes

- SQLModel metadata is created automatically on app startup via `SQLModel.metadata.create_all(engine)`.
- CORS is configured for local frontend development, including `127.0.0.1:5500` and private network addresses.
- This is an active backend project and is still being expanded with more features.

## Roadmap

Planned next steps include:

- user roles (student, lecturer, admin)
- course and enrollment management
- timetables and deadlines
- messaging and study groups
- database migrations with Alembic
- automated tests
- richer permission checks and admin-only routes

## License

This project is currently for personal / learning / portfolio use unless otherwise stated by the project owner.
