"""
Flask Application
=================

This is the default entrypoint for our application.
Flask tutorial: https://flask.palletsprojects.com/en/2.2.x/tutorial/

"""

from os import environ
import os
from typing import Dict, Literal, Optional

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    Response,
    request,
)

from .utils import get_version
from .db import init_db
from .logging import logger, init_logging


def create_app(config: Optional[Dict] = None) -> Flask:
    """
    Application factory for creating a new Flask instance.

    :param name: The name of the application.
    """
    flask_app = Flask(__name__, instance_relative_config=True)

    flask_app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # Load the instance config if it exists, when not testing
    if config is None:
        flask_app.config.from_pyfile('config.py', silent=True)
    else:
        flask_app.config.from_mapping(config)

    # Initialize logging
    init_logging(flask_app)

    # Ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    # Initialize the database connection.
    init_db(flask_app)

    # A simple page that says hello for testing purpose
    @flask_app.route('/hello')
    def hello():
        return 'Hello, World!'

    #from . import auth
    #flask_app.register_blueprint(auth.bp)
    from .auth import init_auth
    init_auth(flask_app)


    from . import items
    flask_app.register_blueprint(items.bp)
    flask_app.add_url_rule('/', endpoint='index')

    return flask_app


# Load environment variables from .env file, if present. See the `dotenv` file for a
# template and how to use it.
load_dotenv()

# Create the Flask application.
flask_app = create_app()

@flask_app.route("/server-info")
def server_info() -> Response:
    """
    A simple endpoint for checking the status of the server.

    This is useful for monitoring the server, and for checking that the server is
    running correctly.
    """

    # Check if the database is connectable.
    database_ping = False
    try:
        from .db import db # pylint: disable=import-outside-toplevel
        database_ping = db.connection.admin.command("ping").get("ok", False) and True
    except Exception as exc: # pylint: disable=broad-except
        logger.warning("Error querying mongodb server: %r", exc, exc_info=True, 
        extra=flask_app.config.get_namespace("MONGODB"))

    response = {
        "database_connectable": database_ping,
        "version": get_version(),
        "build_date": environ.get("BUILD_DATE", None)
    }

    # Response with pong if ping is provided.
    ping = request.args.get("ping", None)
    if ping is not None:
        response["pong"] = f"{ping}"

    return jsonify(response)
