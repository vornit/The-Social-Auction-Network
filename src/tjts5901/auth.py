import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from mongoengine import DoesNotExist

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, load the user object from database
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.objects.get(id=user_id)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Page for registering the user
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        #User email and password are required
        if not    email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'

        #If there was no problem in email or password
        if error is None:
            try:
                #Create a user with email and password, password will be hashed
                user = User(
                    email=email,
                    password=generate_password_hash(password)
                )
                user.save()
            #Throw Error if anykind of exception occurred
            except Exception as exc:
                error = f"Error when creating user: {exc!s}"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Page for logging in the user
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None
        #Look for email form the existing user emails
        try:
            user = User.objects.get(email=email)
        except DoesNotExist:
            error = 'Incorrect username.'

        #Check if the password is correct
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        #No errors so we can proceed to the auction page
        if error is None:
            session.clear()
            session['user_id'] = str(user['id'])
            flash(f"Hello {email}, You have been logged in.")
            return redirect(url_for('index'))

        #Show flash if there was problem logging in at some point
        print("Error logging in:", error)
        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """
    Logout function
    """
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('index'))
