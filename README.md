# Student Hub Backend

This repository contains the backend API for the Student Hub project, a student-focused platform designed to support academic, administrative, and campus community workflows.

Repository URL:

```bash
git clone https://github.com/Optimus523/student-hub-backend.git
```

The backend is built with FastAPI and SQLModel, and it currently supports user authentication, announcement management, and secure database-backed storage using PostgreSQL.

## Overview

Student Hub is intended to become a central platform for students to access information and services such as:

- academic updates and notices
- campus announcements
- student accounts and credentials
- administrative communication
- future course, timetable, and community features

This repository focuses on the API layer that powers those experiences.

## Current status

The project is in active development, but the backend already includes the following working features:

- user registration with validation
- unique username checks
- secure password hashing using Argon2
- JWT-based login and token verification
- protected announcement routes requiring authentication
- announcement creation, viewing, and deletion
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

## Project structure

```text
student-hub-backend/
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
├── venv/              # local virtual environment, excluded from git
└── .env               # local secrets, excluded from git
```

## Architecture notes

The backend is organized into clear layers:

- `app/models/` defines the database tables
- `app/schemas/` defines request and response validation models
- `app/routers/` contains endpoint handlers grouped by feature
- `app/database.py` manages the SQLModel engine and database session lifecycle
- `app/security.py` handles password hashing, JWT creation, and protected-route validation
- `app/main.py` configures the FastAPI app, CORS, and router registration

This separation keeps the project easier to extend as more features are added.

## Prerequisites

Before running this project locally, make sure you have:

- Python 3.10 or newer
- PostgreSQL installed and running
- a local database created for the project
- a virtual environment tool available for Python

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/Optimus523/student-hub-backend.git
cd student-hub-backend
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

### 4. Create the PostgreSQL database

Open PostgreSQL and create a database such as:

```sql
CREATE DATABASE student_hub;
```

### 5. Configure environment variables

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Then set your values in `.env`:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/student_hub
SECRET_KEY=your-secret-key-here
```

Notes:

- Never commit `.env`
- Never commit `venv/`
- Use a strong random value for `SECRET_KEY`
- If your database password contains special characters, URL-encode them correctly

## Running the app

Start the API with:

```bash
fastapi dev app/main.py
```

Or run with uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open the docs in your browser:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API overview

### Authentication endpoints

#### Register user

```http
POST /users/
```

Example request body:

```json
{
    "username": "edwin",
    "password": "secret123"
}
```

Rules:

- username must be between 3 and 30 characters
- username may only contain letters, numbers, and underscores
- password must be between 8 and 128 characters
- duplicate usernames return `409 Conflict`

#### Login

```http
POST /login/
```

This endpoint accepts OAuth2 password form data:

```text
username=edwin&password=secret123
```

Example response:

```json
{
    "access_token": "<jwt-token>",
    "token_type": "bearer"
}
```

### Announcement endpoints

#### Create announcement

```http
POST /announcements/
```

Requires a valid JWT token in the `Authorization` header.

Example request body:

```json
{
    "title": "Exam timetable",
    "body": "The exam timetable is now available on the notice board."
}
```

#### Get all announcements

```http
GET /announcements/
```

#### Get single announcement

```http
GET /announcements/{id}
```

#### Delete announcement

```http
DELETE /announcements/{id}
```

Requires authentication and ownership/auth validation through the current user dependency.

## Authentication and security

This backend uses JWT-based authentication to protect sensitive routes.

Current security features include:

- password hashing with Argon2
- storage of only hashed passwords
- token generation on successful login
- token validation through a dependency
- restricted access to announcement creation and deletion routes

Example header:

```http
Authorization: Bearer <your-token>
```

## Database models

### User model

Fields:

- `id`: primary key
- `username`: unique login name
- `hashed_password`: securely hashed user password

### Announcement model

Fields:

- `id`: primary key
- `title`: short headline or title
- `body`: content of the announcement
- `author_id`: foreign key linking the announcement to the author user

## Notes

- SQLModel metadata is created automatically on startup via `SQLModel.metadata.create_all(engine)`.
- CORS is configured for local frontend testing, including `127.0.0.1:5500` and private-network addresses.
- The app is actively evolving and is intended to grow into a broader student platform.

## Roadmap

Planned future improvements include:

- role-based access control
- student, admin, and lecturer roles
- course and enrollment management
- timetables and deadlines
- messaging and study groups
- database migrations with Alembic
- unit/integration tests
- more refined permission checks and admin-only routes

## License

This project is currently intended for personal, learning, and portfolio use unless otherwise specified by the project owner.

## Contributing

This repo is still under active development, so contributions are welcome if the project direction and implementation approach align with the goals of the platform.

If you are working on the project locally, make sure to keep your `.env` and `venv/` out of version control and push only the application code, configuration templates, and documentation.
