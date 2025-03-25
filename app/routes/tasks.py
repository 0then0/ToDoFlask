from flask import Blueprint, jsonify, request

from app import db
from app.models.tag import Tag
from app.models.task import Task, task_tag
from app.schemas import tag_schema, tags_schema, task_schema, tasks_schema

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

    if "tags" in data:
        tags_data = data["tags"]
        for tag_data in tags_data:
            tag = Tag.query.filter_by(name=tag_data["name"]).first()
            if not tag:
                tag = Tag(name=tag_data["name"])
                db.session.add(tag)
            task.tags.append(tag)

    db.session.add(task)
    db.session.commit()
    result = task_schema.dump(task)
    return jsonify(result), 201


@bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    errors = task_schema.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    task_data = task_schema.load(data, partial=True)
    if "title" in task_data:
        task.title = task_data["title"]
    if "description" in task_data:
        task.description = task_data.get("description")
    if "completed" in task_data:
        task.completed = task_data["completed"]
    if "tags" in data:
        task.tags.clear()
        for tag_data in data["tags"]:
            tag = Tag.query.filter_by(name=tag_data["name"]).first()
            if not tag:
                tag = Tag(name=tag_data["name"])
                db.session.add(tag)
            task.tags.append(tag)

    db.session.commit()
    result = task_schema.dump(task)
    return jsonify(result)


@bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {task_id} deleted"}), 200
