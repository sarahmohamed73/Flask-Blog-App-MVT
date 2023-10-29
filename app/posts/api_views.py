from flask_restful import Resource, marshal_with, abort
from flask import  make_response
from app.posts.serializers import post_serlizer
from app.models import Post, db
from app.posts.parser import post_parser

# Crud Operations
class PostList(Resource):
  # Get All Post
  @marshal_with(post_serlizer)
  def get(self):
    posts = Post.get_all_objects()
    return posts, 200
  
  # Post Post
  @marshal_with(post_serlizer)
  def post(self):
    post_args = post_parser.parse_args()
    post = Post.create_post(post_args)
    return post, 201
  
class PostResource(Resource):
  # Get Specific Post
  @marshal_with(post_serlizer)
  def get(self, post_id):
    post = Post.get_specific_post(post_id)
    return post, 200

  # Update Post 
  @marshal_with(post_serlizer)
  def put(self, post_id):
    post = Post.get_specific_post(post_id)
    if post:
      post_args = post_parser.parse_args()
      post.title = post_args['title']
      post.body = post_args['body']
      post.image = post_args['image']
      post.category_id = post_args['category_id']
      db.session.add(post)
      db.session.commit()
      return post, 200
    abort(404, message='Post Not Found')

  # Delete Post
  @marshal_with(post_serlizer)
  def delete(self, post_id):
    post = Post.get_specific_post(post_id)
    if post:
      db.session.delete(post)
      db.session.commit()
      response = make_response("Deleted Successfully", 204)
      return response, 200
    abort(404, message='Post Not Found')