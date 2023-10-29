from flask import Flask
from app.models import db
from app.config import projectConfig as AppConfig
from flask_migrate import Migrate
from flask import render_template
from flask_restful import Api
from app.posts.api_views import PostList, PostResource
from app.categories.api_views import CategoryList, CategoryResource

def create_app(config_name = 'dev'):
  app = Flask(__name__)
  current_config = AppConfig[config_name]
  app.config['SQLALCHEMY_DATABASE_URI'] = current_config.SQLALCHEMY_DATABASE_URI
  app.config['SQLALCHEMY_DATABASE_URI'] = current_config
  app.config.from_object(current_config)

  db.init_app(app)

  migrate = Migrate(app, db, render_as_batch=True)

  api = Api(app)

  api.add_resource(PostList, '/api/posts')
  api.add_resource(PostResource, '/api/posts/<int:post_id>')
  api.add_resource(CategoryList, '/api/categories')
  api.add_resource(CategoryResource, '/api/categories/<int:category_id>')

  # Contact
  def contact():
    return render_template('information/contact.html')

  # About
  def about():
    return render_template('information/about.html')

  # Error Page
  @app.errorhandler(404)
  def page_not_found(error):
    print(error)
    return  render_template('errors/page_not_found.html')

  app.add_url_rule("/contact", view_func=contact, endpoint='contact', methods=['GET'])
  app.add_url_rule("/about", view_func=about, endpoint='about', methods=['GET'])
  
  # Post BluePrint
  from app.posts import post_blueprint
  app.register_blueprint(post_blueprint)

   # Post BluePrint
  from app.categories import category_blueprint
  app.register_blueprint(category_blueprint)

  return app