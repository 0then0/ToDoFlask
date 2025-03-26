from flask import Blueprint, jsonify, request
from sqlalchemy import asc, desc

from app import db
from app.models.tag import Tag
from app.models.task import Task, task_tag
from app.schemas import tag_schema, tags_schema, task_schema, tasks_schema

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@bp.route("/", methods=["GET"])
def get_tasks():
    query = Task.query

    completed_str = request.args.get("completed")
    if completed_str is not None:
        completed = completed_str.lower() == "true"
        query = query.filter(Task.completed == completed)

    sort = request.args.get("sort", default="id", type=str)
    order = request.args.get("order", default="asc", type=str)

    sortable_fields = {
        "id": Task.id,
        "title": Task.title,
        "created_at": Task.created_at,
        "completed": Task.completed,
    }

    if sort in sortable_fields:
        if order.lower() == "desc":
            query = query.order_by(desc(sortable_fields[sort]))
        else:
            query = query.order_by(asc(sortable_fields[sort]))
    else:
        query = query.order_by(asc(Task.id))

    tasks = query.all()
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
