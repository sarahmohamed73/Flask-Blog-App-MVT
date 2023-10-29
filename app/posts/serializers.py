from flask_restful import fields
from app.categories.serializers import category_serlizer

post_serlizer = {
  "id": fields.Integer,
  "title": fields.String,
  "body": fields.String,
  "image": fields.String,
  "category_id": fields.Integer,
  "category_name": fields.Nested(category_serlizer)
}