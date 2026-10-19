# Student Hub Backend

This repository contains the backend API for the Student Hub project, a student-focused platform designed to support academic, administrative, and campus community workflows.

Repository URL:

    git clone https://github.com/Optimus523/student-hub-backend.git

The backend is built with FastAPI and SQLModel, and it currently supports user authentication, user profile management, announcement management, assignment tracking, profile picture uploads, and secure database-backed storage using PostgreSQL.

## Overview

Student Hub is intended to become a central platform for students to access information and services such as:

- academic updates and notices
- campus announcements
- student accounts and credentials
- assignments and deadlines
- profile customization and avatars
- administrative communication
- future course, timetable, and community features

This repository focuses on the API layer that powers those experiences.

## Current status

The project is in active development, but the backend already includes the following working features:

- user registration with validation
- unique username checks
- secure password hashing using Argon2
- JWT-based login and token verification
- user profile retrieval (`/users/me`)
- username and password update with current-password verification
- profile picture upload with file validation and disk storage
- protected announcement routes requiring authentication
- announcement creation, viewing, and deletion (author-only delete)
- protected assignment routes requiring authentication
- assignment creation, viewing, and deletion (author-only delete)
- assignments sorted by due date (soonest first)
- PostgreSQL integration through SQLModel
- automatic table creation on application startup
- CORS setup for local frontend testing

## Tech stack

- Python 3.10+
- FastAPI
- SQLModel
- PostgreSQL
- psycopg
- python-dotenv
- pwdlib[argon2]
- PyJWT
- python-multipart (for file uploads)
- uvicorn (dev server)

## Project structure

    student-hub-backend/
    ├── app/
    │   ├── __init__.py
    │   ├── database.py
    │   ├── main.py
    │   ├── security.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── announcement.py
    │   │   ├── assignment.py
    │   │   └── user.py
    │   ├── routers/
    │   │   ├── __init__.py
    │   │   ├── announcements.py
    │   │   ├── assignments.py
    │   │   ├── auth.py
    │   │   └── users.py
    │   └── schemas/
    │       ├── __init__.py
    │       ├── announcement.py
    │       ├── assignment.py
    │       └── user.py
    ├── uploads/              # created at startup, ignored by git
    │   └── avatars/
    ├── .env.example
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── venv/                 # local virtual environment, excluded from git
    └── .env                  # local secrets, excluded from git

## Architecture notes

The backend is organized into clear layers:

- `app/models/` defines the database tables
- `app/schemas/` defines request and response validation models
- `app/routers/` contains endpoint handlers grouped by feature
- `app/database.py` manages the SQLModel engine and database session lifecycle
- `app/security.py` handles password hashing, JWT creation, and protected-route validation
- `app/main.py` configures the FastAPI app, CORS, static file mounts, and router registration

This separation keeps the project easier to extend as more features are added.

## Prerequisites

Before running this project locally, make sure you have:

- Python 3.10 or newer
- PostgreSQL installed and running
- a local database created for the project
- a virtual environment tool available for Python

## Local setup

### 1. Clone the repository

    git clone https://github.com/Optimus523/student-hub-backend.git
    cd student-hub-backend

### 2. Create and activate a virtual environment

    python3 -m venv venv
    source venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Create the PostgreSQL database

Open PostgreSQL and create a database such as:

    CREATE DATABASE student_hub;

### 5. Configure environment variables

Create a local `.env` file from the example:

    cp .env.example .env

Then set your values in `.env`:

    DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/student_hub
    SECRET_KEY=your-secret-key-here

Notes:

- Never commit `.env`
- Never commit `venv/`
- Use a strong random value for `SECRET_KEY`
- If your database password contains special characters, URL-encode them correctly

## Running the app

Start the API with:

    fastapi dev app/main.py

Or run with uvicorn directly:

    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Then open the docs in your browser:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The first time the app runs, SQLModel will create all tables automatically. It will also create the `uploads/avatars/` directory if it doesn't exist.

## API overview

### Authentication endpoints

#### Register user

    POST /users/

Example request body:

    {
        "username": "edwin",
        "password": "secret123"
    }

Rules:

- username must be between 3 and 30 characters
- username may only contain letters, numbers, and underscores
- password must be between 8 and 128 characters
- duplicate usernames return `409 Conflict`

#### Login

    POST /login/

This endpoint accepts OAuth2 password form data:

    username=edwin&password=secret123

Example response:

    {
        "access_token": "<jwt-token>",
        "token_type": "bearer",
        "user_id": 1,
        "username": "edwin"
    }

### User endpoints

#### Get current user

    GET /users/me

Requires a valid JWT token in the `Authorization` header.

Example response:

    {
        "id": 1,
        "username": "edwin",
        "avatar_url": "/uploads/avatars/user_1_abc12345.jpg"
    }

`avatar_url` is `null` if the user hasn't uploaded a picture.

#### Update current user

    PATCH /users/me

Requires a valid JWT token.

Example request bodies:

Change username only:

    {
        "username": "edwin_new"
    }

Change password:

    {
        "current_password": "secret123",
        "new_password": "newsecret456"
    }

Rules:

- if `username` is provided, it must be unique (`409 Conflict` otherwise)
- if `new_password` is provided, `current_password` is required and must verify
- returns `400 Bad Request` if nothing changes

#### Upload avatar

    POST /users/me/avatar

Requires a valid JWT token. Accepts `multipart/form-data` with a single `file` field.

Limits:

- max 2 MB
- allowed types: `image/jpeg`, `image/png`, `image/webp`

Behavior:

- old avatar (if any) is deleted from disk
- new file is saved as `uploads/avatars/user_{id}_{hash}.{ext}`
- `user.avatar_url` is updated to the served path
- response includes the new `avatar_url`

Uploaded avatars are served at `http://127.0.0.1:8000/uploads/avatars/<filename>`.

### Announcement endpoints

#### Create announcement

    POST /announcements/

Requires a valid JWT token in the `Authorization` header.

Example request body:

    {
        "title": "Exam timetable",
        "body": "The exam timetable is now available on the notice board."
    }

#### Get all announcements

    GET /announcements/

Returns each announcement with `author_username` and `created_at`.

#### Get single announcement

    GET /announcements/{id}

#### Delete announcement

    DELETE /announcements/{id}

Requires authentication. Only the original author may delete.

Rules:

- returns `403 Forbidden` if the caller is not the author
- returns `404 Not Found` if the announcement doesn't exist

### Assignment endpoints

#### Create assignment

    POST /assignments/

Requires a valid JWT token in the `Authorization` header.

Example request body:

    {
        "title": "Assignment 3: Binary Trees",
        "description": "Implement a BST with insert, delete, and traversal.",
        "course_code": "CS201",
        "due_date": "2026-10-21T23:59:00Z"
    }

#### Get all assignments

    GET /assignments/

Returns all assignments sorted by `due_date` ascending. Each item includes `author_username` and `created_at`.

#### Get single assignment

    GET /assignments/{id}

#### Delete assignment

    DELETE /assignments/{id}

Requires authentication. Only the original author may delete.

Rules:

- returns `403 Forbidden` if the caller is not the author
- returns `404 Not Found` if the assignment doesn't exist

## Authentication and security

This backend uses JWT-based authentication to protect sensitive routes.

Current security features include:

- password hashing with Argon2
- storage of only hashed passwords
- token generation on successful login
- token validation through a dependency
- author-only deletion of announcements and assignments
- current-password verification before password change
- upload validation (file type and size)

Example header:

    Authorization: Bearer <your-token>

## Database models

### User model

Fields:

- `id`: primary key
- `username`: unique login name
- `hashed_password`: securely hashed user password
- `avatar_url`: optional path to uploaded avatar (`null` if none)

### Announcement model

Fields:

- `id`: primary key
- `title`: short headline or title
- `body`: content of the announcement
- `author_id`: foreign key linking the announcement to the author user
- `created_at`: UTC timestamp of when the announcement was created

### Assignment model

Fields:

- `id`: primary key
- `title`: assignment title
- `description`: details of the assignment
- `course_code`: course identifier (e.g. "CS201")
- `due_date`: when the assignment is due
- `author_id`: foreign key linking the assignment to the author user
- `created_at`: UTC timestamp of when the assignment was created

## File uploads

Uploaded avatars are stored in `uploads/avatars/` and served as static files at `/uploads/...`.

The uploads directory is:

- created automatically at startup
- excluded from git via `.gitignore`
- not backed up automatically — back it up separately if you care about user data

## Notes

- SQLModel metadata is created automatically on startup via `SQLModel.metadata.create_all(engine)`.
- CORS is configured for local frontend testing, including `127.0.0.1:5500` and private-network addresses.
- The app is actively evolving and is intended to grow into a broader student platform.
- **If you add a new column to an existing model, `create_all()` will not alter the table.** Either drop the table (wipes data) or run `ALTER TABLE` manually. Alembic is planned for proper migrations.

## Roadmap

Planned future improvements include:

- role-based access control (admin/student/lecturer)
- restrict announcement/assignment creation to admins
- course and enrollment management
- timetables and deadlines UI (backend ready)
- grades and results
- messaging and study groups
- database migrations with Alembic
- unit/integration tests
- pagination for list endpoints
- search and filtering (e.g. assignments by course, announcements by date)

## License

This project is currently intended for personal, learning, and portfolio use unless otherwise specified by the project owner.

## Contributing

This repo is still under active development, so contributions are welcome if the project direction and implementation approach align with the goals of the platform.

If you are working on the project locally, make sure to keep your `.env`, `venv/`, and `uploads/` out of version control and push only the application code, configuration templates, and documentation.
