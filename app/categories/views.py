from flask import  request,render_template, redirect, url_for
from app.models import db
from app.models import Category
from app.categories import category_blueprint


@category_blueprint.route('hello')
def helloworld():
  return "<h1>Hello World Caaaat!</h1>"

@category_blueprint.route('', endpoint='index')
def index():
  categories = Category.get_all_objects()
  return render_template('categories/index.html', categories=categories)

# Create category
@category_blueprint.route('/create', endpoint='create', methods=['GET', 'POST'] )
def create():
  categories = Category.get_all_objects()
  if request.method == 'POST':
    print('Received Data', request.form)
    category = Category(name=request.form['name'])
    category.save_category()
    return redirect(url_for('categories.index'))
  return render_template('categories/create.html', categories=categories)

# Get category
@category_blueprint.route('<int:id>', endpoint='show', methods=['GET'])
def get_category(id):
  category = Category.query.get_or_404(id)
  if category:
    return render_template('categories/show.html', category=category)
  else:
    return 404
  
# Delete category
@category_blueprint.route('<int:id>/delete', endpoint='delete', methods=['GET'])
def delete_category(id):
  category = Category.query.get_or_404(id)
  if category:
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.index'))
  else:
    return 404

# Edit category
@category_blueprint.route('<int:id>/edit', endpoint='edit', methods=['GET', 'POST'])
def edit_category(id):
  category = Category.query.get_or_404(id)
  if request.method == 'POST':
    category.name = request.form['name']
    db.session.commit()
    return redirect(category.get_show_url)
  return render_template('categories/edit.html', category=category)