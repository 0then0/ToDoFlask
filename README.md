# ToDo REST API

A simple ToDo application built with Flask and PostgreSQL.

## Features

- Create, read, update, and delete tasks (CRUD)
- Track task creation and update timestamps
- Assign tags to tasks with many-to-many relationship
- Filter tasks by completion status
- Sort tasks by various fields (id, title, created_at, completed)
- Store tasks and tags in a PostgreSQL database

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/0then0/ToDoFlask
   cd ToDoFlask
   ```

2. **Create a virtual environment and install dependencies:**

   ```sh
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

   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the application:**
   ```sh
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

**Query Parameters for GET /api/tasks/**:

- `completed`: Boolean (e.g., `true` or `false`) - Filter tasks by completion status
- `sort`: String (e.g., `id`, `title`, `created_at`, `completed`) - Field to sort by
- `order`: String (e.g., `asc`, `desc`) - Sort order (default: `asc`)

**Task Fields:**

- `id`: Integer (read-only)
- `title`: String (required, max 100 chars)
- `description`: String (optional)
- `completed`: Boolean (default: `false`)
- `created_at`: DateTime (read-only)
- `updated_at`: DateTime (read-only)
- `tags`: List of tags (optional), (e.g., [{"name": "work"}])

**Examples:**

- `GET /api/tasks?completed=false` - Get all incomplete tasks
- `GET /api/tasks?sort=created_at&order=desc` - Sort tasks by creation date in descending order
- `POST /api/tasks/`:

```json
{
	"title": "Learn Flask",
	"description": "Build a REST API",
	"tags": [{ "name": "work" }, { "name": "learning" }]
}
```
