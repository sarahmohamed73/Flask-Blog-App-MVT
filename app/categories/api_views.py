from flask_restful import Resource, marshal_with, abort
from flask import  make_response
from app.categories.serializers import category_serlizer
from app.models import Category, db
from app.categories.parser import category_parser

# Crud Operations
class CategoryList(Resource):
  # Get All Categories
  @marshal_with(category_serlizer)
  def get(self):
    categories = Category.get_all_objects()
    return categories, 200
  
  # Post Category
  @marshal_with(category_serlizer)
  def post(self):
    category_args = category_parser.parse_args()
    category = Category.create_category(category_args)
    return category, 201
  
class CategoryResource(Resource):
  # Get Specific Category
  @marshal_with(category_serlizer)
  def get(self, category_id):
    category = Category.get_specific_category(category_id)
    return category, 200

  # Update Category 
  @marshal_with(category_serlizer)
  def put(self, category_id):
    category = Category.get_specific_category(category_id)
    if category:
      category_args = category_parser.parse_args()
      category.name = category_args['name']
      db.session.add(category)
      db.session.commit()
      return category, 200
    abort(404, message='Category Not Found')

  # Delete Category
  @marshal_with(category_serlizer)
  def delete(self, category_id):
    categoty = Category.get_specific_category(category_id)
    if categoty:
      db.session.delete(categoty)
      db.session.commit()
      response = make_response("Deleted Successfully", 204)
      return response, 200
    abort(404, message='Category Not Found')