from flask import Blueprint, jsonify, request

from app import db
from app.models.task import Task
from app.schemas import task_schema, tasks_schema

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    return jsonify(result)


@bp.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    errors = task_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    task_data = task_schema.load(data)
    task = Task(title=task_data["title"], description=task_data.get("description"))
    db.session.add(task)
    db.session.commit()

    result = task_schema.dump(task)
    return jsonify(result), 201
