# ToDo REST API

A simple ToDo application built with Flask and PostgreSQL.

## Features

- Create, read, update, and delete tasks
- Store tasks in a PostgreSQL database
- Basic CRUD operations via RESTful endpoints

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup

1. **Clone the repository:**

   ```
   git clone https://github.com/0then0/ToDoFlask
   cd ToDoFlask
   ```

2. **Create a virtual environment and install dependencies:**

   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL:**

   - Create a database (e.g., `todo_db`).
   - Update the `.env` file with your database credentials:
     ```
     DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
     SECRET_KEY=your-secret-key
     ```

4. **Initialize the database:**

   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the application:**
   ```
   python run.py
   ```

## API Endpoints

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| GET    | `/api/tasks/`     | Get all tasks       |
| POST   | `/api/tasks/`     | Create a new task   |
| PUT    | `/api/tasks/<id>` | Update a task by ID |
| DELETE | `/api/tasks/<id>` | Delete a task by ID |
| GET    | `/api/tags/`      | Get all tags        |

**Task Fields:**

- `id`: Integer (read-only)
- `title`: String (required)
- `description`: String (optional)
- `completed`: Boolean (default: false)
- `created_at`: DateTime (read-only)
- `updated_at`: DateTime (read-only)
- `tags`: List of tags (e.g., [{"name": "work"}])

Example POST request:

```json
{
	"title": "Learn Flask",
	"description": "Build a REST API"
}
```
