# Task Manager API

A FastAPI task management API with user authentication, role based access, and PostgreSQL persistence.

## Requirements

- Python 3.10 or newer
- A virtual environment is recommended
- PostgreSQL 13 or newer

## Setup

from the project directory:

```bash
cd /Users/ayahabdullah/Downloads/task-manager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root and set a secret key:

```env
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/task_manager
```

To generate a random key on macOS or Linux:

```bash
echo "SECRET_KEY=$(openssl rand -hex 32)" > .env
```

The application reads `DATABASE_URL` from `.env`. The default value is
`postgresql+psycopg://postgres:postgres@localhost:5432/task_manager`.

Create the PostgreSQL database before starting the API:

```bash
createdb task_manager
```

If your PostgreSQL username, password, host, port, or database name differs,
update `DATABASE_URL` accordingly. For example:

```env
DATABASE_URL=postgresql+psycopg://myuser:mypassword@localhost:5432/my_database
```

The tables are created automatically when the API starts. This application does
not migrate existing SQLite data automatically; export and import the data if
you need to preserve it.

## Create the First Admin

Administrators cannot be created through the public API for security . Create the first one with:

```bash
python create_admin.py
```

The script prompts for an admin username, email, and password.

## Run the API

Start the development server with:

```bash
uvicorn main:app --reload
```

The API is available at:

- http://127.0.0.1:8000
- Interactive Swagger documentation: http://127.0.0.1:8000/docs


main.py will run the code but not uvicorn. 

## Authentication Workflow

1. Register a regular user with `POST /auth/register`.
2. Log in with `POST /auth/login` to receive an access token.
3. In `/docs`, click **Authorize** and enter the token.
4. Use the authenticated task endpoints.

The login endpoint uses OAuth2 form data: send `username` and `password`, not a JSON body.

## Main Endpoints

### Authentication

- `POST /auth/register` - Register a regular user
- `POST /auth/login` - Log in and receive an access token
- `GET /auth/me` - Get the authenticated user

### Tasks

- `POST /tasks` - Create a task
- `GET /tasks` - List accessible tasks
- `GET /tasks/{task_id}` - Get a task
- `PATCH /tasks/{task_id}` - Update a task
- `PATCH /tasks/{task_id}/complete` - Mark a task as complete
- `DELETE /tasks/{task_id}` - Delete a task

Task list results support optional `task_status`, `priority`, `skip`, and `limit` query parameters.

## Project Structure as mentioned in the asigntment 

```text
main.py                 FastAPI application entry point
create_admin.py         Command-line admin creation script
app/config.py           Application settings
app/database.py         Database setup and sessions
app/models.py           SQLModel database models
app/security.py         Password hashing and JWT handling
app/routers/auth.py     Authentication routes
app/routers/tasks.py    Task routes
app/dtos/               Request and response schemas
```
