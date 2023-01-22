"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user_page():
    return render_template('new_user.html')

@app.route('/users', methods=['POST'])
def create_user():
    first_name = request.form.get('first-name')
    if not first_name:
        flash('First Name must not be blank')
        return redirect('/users/new')
    last_name = request.form.get('last-name')
    if not last_name:
        flash('Last Name must not be blank')
        return redirect('/users/new')
    img_url = request.form.get('img-url') or None
    new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    first_name = request.form.get('first-name')
    if not first_name:
        flash('First Name must not be blank')
        return redirect(f'/users/{user.id}/edit')
    last_name = request.form.get('last-name')
    if not last_name:
        flash('Last Name must not be blank')
        return redirect(f'/users/{user.id}/edit')
    img_url = request.form.get('img-url') or None
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img_url or None
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')