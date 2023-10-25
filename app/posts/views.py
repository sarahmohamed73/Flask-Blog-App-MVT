from flask import  request,render_template, redirect, url_for
from app.models import db
from app.models import Post
from app.models import Category
from app.posts import post_blueprint
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_blueprint.route('hello')
def helloworld():
  return "<h1>Hello World!</h1>"

@post_blueprint.route('', endpoint='index')
def index():
  posts = Post.get_all_objects()
  return render_template('posts/index.html', posts=posts)

# Create Post
@post_blueprint.route('/create', endpoint='create', methods=['GET', 'POST'] )
def create():
  categories = Category.get_all_objects()
  if request.method == 'POST':
    print('Received Data', request.form)
    if 'image' in request.files:
      file = request.files['image']
      if file.filename != '':
        if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          current_directory = os.path.dirname(__file__)
          destination = os.path.abspath(os.path.join(current_directory, "../../app/static/posts/images"))
          destination_path = os.path.join(destination, filename)
          print('DES:' , destination_path)
          file.save(destination_path)
      else:
        filename = None
    
    post = Post(title=request.form['title'], body=request.form['body'], image=filename, category_id=request.form['category_id'])
    post.save_post()
    return redirect(url_for('posts.index'))
  return render_template('posts/create.html', categories=categories)

# Get Post
@post_blueprint.route('/posts/<int:id>', endpoint='show', methods=['GET'])
def get_post(id):
  post = Post.query.get_or_404(id)
  if post:
    return render_template('posts/show.html', post=post)
  else:
    return 404
  
# Delete Post
@post_blueprint.route('/posts/<int:id>/delete', endpoint='delete', methods=['GET'])
def delete_post(id):
  post = Post.query.get_or_404(id)
  if post:
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))
  else:
    return 404

# Edit Post
@post_blueprint.route('/posts/<int:id>/edit', endpoint='edit', methods=['GET', 'POST'])
def edit_post(id):
  post = Post.query.get_or_404(id)
  categories = Category.get_all_objects()
  if request.method == 'POST':
    print('Received Data', request.form)
    post.title = request.form['title']
    post.body = request.form['body']
    post.category_id = request.form['category_id']
    file = request.files['image']
    if file.filename != '':
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        current_directory = os.path.dirname(__file__)
        destination = os.path.abspath(os.path.join(current_directory, "../../app/static/posts/images"))
        destination_path = os.path.join(destination, filename)
        print('DES:' , destination_path)
        file.save(destination_path)
        post.image = filename
    else:
      filename = None
    
    db.session.commit()
    return redirect(post.get_show_url)
  return render_template('posts/edit.html', post=post, categories=categories)