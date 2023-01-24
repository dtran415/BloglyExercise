"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'

connect_db(app)
db.create_all()

# user routes
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

# post routes
@app.route('/users/<int:user_id>/posts/new')
def create_post_page(user_id):
    user = User.query.get_or_404(user_id)
    header = f'Add Post for {user.full_name}'
    action = f'/users/{user.id}/posts'
    tags = Tag.query.all()
    return render_template('post_add_or_edit.html', header=header, user=user, action=action, post_title='',
                           post_content='', button_text='Add', tags = tags)

@app.route('/users/<int:user_id>/posts', methods=['POST'])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    
    title = request.form.get('title')
    if not title:
        flash('Please input a title')
        return redirect(f'/users/{user.id}/posts/new')
    content = request.form.get('content')
    if not content:
        flash('Please input content for this post')
        return redirect(f'/users/{user.id}/posts/new')
    
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=title, content=content, user_id=user.id, tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    
    return render_template('post_details.html', user=user, post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def edit_post_page(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    
    header = f'Edit Post'
    action = f'/users/{user.id}/posts/{post.id}'
    tags = Tag.query.all()
    post_tags = post.tags
    return render_template('post_add_or_edit.html', header=header, user=user, action=action, post_title=post.title,
                           post_content=post.content, button_text='Edit', tags=tags, post_tags=post_tags)

@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['POST'])
def edit_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    
    title = request.form.get('title')
    if not title:
        flash('Please input a title')
        return redirect(f'/users/{user.id}/posts/{post_id}/edit')
    content = request.form.get('content')
    if not content:
        flash('Please input content for this post')
        return redirect(f'/users/{user.id}/posts/{post_id}/edit')
    
    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/users/{user.id}/posts/{post.id}')

# tag routes
@app.route('/tags/new')
def create_tag_page():
    header = 'Create a Tag'
    action = '/tags'
    return render_template('tags_add_or_edit.html', header=header, action=action, button_text='Add')

@app.route('/tags')
def show_tags_page():
    tags = Tag.query.all()
    return render_template('tags_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_posts_for_tags(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags_show_posts.html', tag=tag)

@app.route('/tags', methods=['POST'])
def create_tag():
    name = request.form.get('name')
    if not name:
        flash('Please input a name')
        return redirect('/tags/new')
    
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_page(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    header = 'Edit a tag'
    action = f'/tags/{tag.id}'
    tag_name = tag.name
    return render_template('tags_add_or_edit.html', header=header, action=action, button_text='Edit', tag_name=tag_name)

@app.route('/tags/<int:tag_id>', methods=['POST'])
def edit_tag(tag_id):
    name = request.form.get('name')
    if not name:
        flash('Please input a name')
        return redirect(f'/tags/{tag_id}')
    
    tag = Tag.query.get_or_404(tag_id)
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')