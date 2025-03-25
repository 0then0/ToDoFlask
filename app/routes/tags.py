from flask import Blueprint, jsonify

from app import db
from app.models.tag import Tag
from app.schemas import tags_schema

bp = Blueprint("tags", __name__, url_prefix="/api/tags")


@bp.route("/", methods=["GET"])
def get_tags():
    tags = Tag.query.all()
    result = tags_schema.dump(tags)
    return jsonify(result)
