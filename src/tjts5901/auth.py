import functools
import logging

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, abort
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from werkzeug.security import check_password_hash, generate_password_hash
from sentry_sdk import set_user

from .models import User, Item
from mongoengine import DoesNotExist

bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)

def init_auth(app):
    """
    Integrate authentication into the application
    """
    app.register_blueprint(bp)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.user_loader(load_logged_in_user)
    login_manager.init_app(app)
    logger.debug("Initialized authentication")


def load_logged_in_user(user_id):
    """
    Load a user from the database, given the user's id.
    """
    try:
        user = User.objects.get(id=user_id)
        set_user({"id": str(user.id), "email": user.email})
        "Set sessions user to current user"
    except DoesNotExist:
        logger.error("User not found: %s", user_id)
        return None

    return user

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
                flash("Registeration Successfull")
            #Throw Error if anykind of exception occurred
            except Exception as exc:
                error = f"Error when creating user: {exc!s}"
            else:
                return redirect(url_for("auth.login"))

        print("Could not register user:", error)
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
            error = 'Incorrect email'

        #Check if the password is correct
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        #No errors so we can proceed to the auction page
        if error is None:
            remember_me = bool(request.form.get("remember-me", False))
            if login_user(user, remember=remember_me):

                flash(f"Hello {email}, You have been logged in.")

                next = request.args.get('next')
                # Better check that the user actually clicked on a relative link
                # or else they could redirect you to a malicious website!
                if next is None or not next.startswith('/'):
                    next = url_for('index')

                return redirect(next)
            else:
                error = "Error logging in."

        logger.info("Error logging user in: %r: Error: %s", email, error)
        #Show flash if there was problem logging in at some point
        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """
    Log out the current user.

    Also removes the "remember me" cookie.
    """
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))


@bp.route('/profile/<email>')
@login_required
def profile(email):
    """
    Show the user's profile page for the given email.

    If the email is 'me', then the current user's profile is shown.
    """
    if email == 'me':
        email = current_user.email

    #Set the user by the email, return 404 if the email is incorrect
    user: User = User.objects.get_or_404(email=email)

    # List the items user has created
    items = Item.objects(seller=user).all()

    return render_template('auth/profile.html', user=user, items=items)
