from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db 
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:

            if check_password_hash(user.password, password):
                flash("Logged In", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            
            else:
                flash("Incorrect password.", category="error")
        
        else:
            flash("Email does not exist", category='error')

    return render_template("login.html")

@auth.route("/sign-up", methods=["GET","POST"])
def sign_up():

    if request.method == "POST":

        # get the user inputted data from the form
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # query some data from the database to do a check
        email_exists_check = User.query.filter_by(email=email).first()
        username_exists_check = User.query.filter_by(username=username).first()
        
        if email_exists_check:
            flash("This email have been used previously by a user.", category="error")

        elif username_exists_check:
            flash("This username is already in use.", category="error")
        
        elif password1 != password2:
            flash("Passwords dont match!", category="error")
        
        elif len(password1) < 6:
            flash("Password is too short", category="error")
        
        elif len(email) < 4:
            flash("Email is invalid", category="error")

        # if pass the logic check then add user to database
        else:
            new_user = User(
                email = email,
                username = username,
                password = generate_password_hash(password=password1, method="sha256") # --> store the pasword using sha256 hashing
            )

            # add user
            db.session.add(new_user)
            # commit database changes
            db.session.commit()

            login_user(new_user, remember=True)
            flash("User created !", category="success")
            flash("User Logged in!", category='success')
            return redirect(url_for("views.home"))


    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home')) # - reference the 'home' functions from the view.py file