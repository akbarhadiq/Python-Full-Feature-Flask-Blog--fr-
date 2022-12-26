from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .clean_strip_html import strip_invalid_html
from .models import Post,  User, Comment
from . import db

views = Blueprint("views", __name__)

@views.route("/home")
@views.route("/")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", name=current_user.username, posts=posts, user=current_user)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        blog_post = request.form.get('ckeditor')

        if not title or not blog_post or not title and blog_post:
            flash("Title or post cannot be empty!",category='error')
        
        else:
            clean_post = strip_invalid_html(blog_post)

            # db modelling :
            new_post = Post(
                title = title,
                author = current_user.id,
                post_text = clean_post
            )

            db.session.add(new_post)
            db.session.commit()

            flash("Post successfully created!")
            return redirect(url_for('views.home', user=current_user))

    return render_template("create_post.html", user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        flash("Post does not exist", category='error')

    # check if current user is the author of the post
    elif current_user.id != post.id:
        flash("You did not have permission to delete this post.", category='error')
    
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", category='success')
    
    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exists!", category='error')
        return redirect(url_for('views.home'))

    else:
        post = user.posts
        return render_template("posts.html", user=current_user, posts=post, username=username)

@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash("Comment cannot be empty", category='error')
        redirect(url_for('views.home'))
    
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                comment_text = text,
                author = current_user.id,
                post_id = post_id
            )

            db.session.add(comment)
            db.session.commit()
            flash('Comment added successfully!')
            return redirect(url_for('views.home'))
        else:
            flash('Post does not exist', category='error')
            return redirect(url_for('views.home'))

@views.route("/delete-comments/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("Comment does not exist.", category='error')
        return redirect(url_for('views.home'))
    
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("You do not have permission to delete this comment", category='error')
        return redirect(url_for('views.home'))

    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment successfully deleted!")
        return redirect(url_for('views.home'))
