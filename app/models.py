from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, request, redirect, url_for

db = SQLAlchemy()

class Category(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
  posts= db.relationship('Post', backref='category_name', lazy=True)

  def __str__(self):
    return f"{self.name}"

  @classmethod
  def get_all_objects(cls):
    return cls.query.all()
  
  def save_category(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def create_category(cls, request_form):
    category = cls(**request_form)
    db.session.add(category)
    db.session.commit()
    return category
  
  @classmethod
  def get_specific_category(cls, id):
     return cls.query.get_or_404(id)
  
  @property
  def get_show_url(self):
    return url_for('categories.show', id=self.id)
  
  @property
  def get_delete_url(self):
    return url_for('categories.delete', id=self.id)


class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String)
  body = db.Column(db.String)
  image = db.Column(db.String)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

  @classmethod
  def get_all_objects(cls):
    return cls.query.all()
  
  def save_post(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def create_post(cls, request_form):
    post = cls(**request_form)
    db.session.add(post)
    db.session.commit()
    return post
  
  @classmethod
  def get_specific_post(cls, id):
     return cls.query.get_or_404(id)

  @property
  def get_image_url(self):
    return url_for('static', filename=f'posts/images/{self.image}')
  
  @property
  def get_show_url(self):
    return url_for('posts.show', id=self.id)
  
  @property
  def get_delete_url(self):
    return url_for('posts.delete', id=self.id)