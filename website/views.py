from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Post, User
from . import db
import os

views = Blueprint("views", __name__)

@views.route("/")
def base():
    return render_template("base.html", name="guest")

@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        image = request.files.get('image')
        image_filename = None  

        if not text and not image:
            flash('Post cannot be empty', category='error')
        else:
            if image:
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
                flash('Image uploaded!', category='success')

            if text or image_filename:  # Only create a post if there's text or an image
                post = Post(text=text, image_filename=image_filename, author=current_user.id)
                db.session.add(post)
                db.session.commit()
                flash('Post created!', category='success')
                return redirect(url_for('views.home'))

            return redirect(url_for('views.create_post'))

    return render_template('create_post.html', user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query/filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.id:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
    
    return redirect(url_for('views.home'))

@views.route("/posts/<username>") # dynamic variables in routes are in <> 
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No user with that username exists.", category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=user)