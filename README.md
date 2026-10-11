# Student Hub API

The backend for the Student Hub, a student companion app built around three pillars:

- **Academic:** timetables, deadlines, course materials and grades
- **Admin:** announcements, fees and registration
- **Social and logistics:** messaging, study groups and voice rooms

It is a long-term project, built step by step and not rushed out as a minimum product. This repository holds the API, written with FastAPI and PostgreSQL.

## Status

Early development. What works today:

- Student registration and login with securely hashed passwords
- Announcements: create, list, read one and delete
- Data stored in PostgreSQL, with the database settings kept in a `.env` file

In progress or planned:

- Login that returns an access token (JWT)
- Protecting the create and delete routes so only authorised users can use them
- User roles (student, lecturer, admin)
- Courses, enrollments, timetables and deadlines
- Messaging and study groups
- Database migrations with Alembic and automated tests

## Tech stack

| Part             | Choice                          |
| ---------------- | ------------------------------- |
| Framework        | FastAPI                         |
| Database         | PostgreSQL                      |
| ORM              | SQLModel (on top of SQLAlchemy) |
| Driver           | psycopg 3                       |
| Password hashing | pwdlib with Argon2              |
| Settings         | python-dotenv                   |

## Project layout

```
backend_student_hub/
├── main.py            # app, models, routes
├── security.py        # password hashing and verification
├── requirements.txt   # Python dependencies
├── .env               # local settings (not committed)
└── .env.example       # template for .env
```

As the project grows, the plan is to split `main.py` into routers, models, schemas and services.

## Getting started

### Prerequisites

- Python 3.10 or newer
- PostgreSQL, running locally

### 1. Clone and enter the project

```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Create and activate a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```
pip install -r requirements.txt
```

### 4. Create the database

In `psql`:

```sql
CREATE DATABASE student_hub;
```

### 5. Configure the environment

Copy the template and edit it with your own values:

```
cp .env.example .env
```

`.env` needs one line:

```
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/student_hub
```

If your password contains special characters such as `@`, URL-encode them (`@` becomes `%40`). Never commit `.env`.

### 6. Run the API

```
fastapi dev main.py
```

The tables are created automatically on startup. Open http://127.0.0.1:8000/docs for the interactive documentation, where you can try every route.

## API overview

| Method | Path                  | Purpose                             |
| ------ | --------------------- | ----------------------------------- |
| POST   | `/users`              | Register a new user                 |
| POST   | `/login`              | Log in with a username and password |
| POST   | `/announcements`      | Create an announcement              |
| GET    | `/announcements`      | List all announcements              |
| GET    | `/announcements/{id}` | Get one announcement                |
| DELETE | `/announcements/{id}` | Delete an announcement              |

### Registration rules

- Username: 3 to 30 characters, letters, digits and underscores only. It is stored in lowercase, so `Edwin` and `edwin` are the same user.
- Password: 8 to 128 characters.
- A username that already exists returns `409 Conflict`.

### Login

Login accepts form data, the standard OAuth2 password format, which is also what the **Authorize** button in `/docs` uses. A wrong username and a wrong password return the same `401` message, so the response does not reveal which usernames exist.

### Example requests

Register:

```
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "edwin", "password": "secret123"}'
```

Log in:

```
curl -X POST http://127.0.0.1:8000/login \
  -d "username=edwin&password=secret123"
```

Create an announcement:

```
curl -X POST http://127.0.0.1:8000/announcements \
  -H "Content-Type: application/json" \
  -d '{"title": "Exam timetable", "body": "The timetable is now on the notice board."}'
```

## Security notes

- Passwords are never stored. Only an Argon2 hash with a random salt is saved.
- API responses never include the password hash, because they go through a separate output model.
- Secrets live in `.env`, which is excluded from git.
- At this stage the create and delete routes are open to anyone. Protecting them is the next milestone, so do not expose this version to real users.

## Roadmap

1. Environment-based configuration (done)
2. Users, hashing, registration and login (done)
3. Access tokens and a current-user dependency
4. Protected routes and user roles
5. Courses, enrollments, timetables and deadlines
6. Messaging and study groups
7. Migrations and tests

## About

Built as part of a self-directed journey into software and robotics engineering.
