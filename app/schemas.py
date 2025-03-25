from marshmallow import Schema, fields, validate


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)
    completed = fields.Bool(default=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
