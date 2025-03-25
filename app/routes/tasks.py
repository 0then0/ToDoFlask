from flask import Blueprint, jsonify, request

from app import db
from app.models.task import Task

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify(
        [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
    )


@bp.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    task = Task(title=data["title"], description=data.get("description"))
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 201
