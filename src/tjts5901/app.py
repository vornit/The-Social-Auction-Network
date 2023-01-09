from importlib.metadata import version
from os import environ

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    Response,
    request,
)


def create_app(name=__name__) -> Flask:
    """
    Application factory for creating a new Flask instance.

    :param name: The name of the application.
    """
    new_app = Flask(name)

    return new_app


def get_version() -> str:
    """
    Get the version of the application.

    This is useful for checking the version of the application, and for
    monitoring the application.
    """

    # Get the version from the environment varible. It's setup by CI/CD pipeline.
    ver = environ.get("CI_COMMIT_SHA", None)

    if ver is None:
        # Get the version from the package.
        ver = version(__name__)

    return str(ver)


# Load environment variables from .env file, if present. See the `dotenv` file for a
# template and how to use it.
load_dotenv()

# Create the Flask application.
app = create_app()


@app.route("/")
def index():
    return "Hello, world!"


@app.route("/server-status")
def server_status() -> Response:
    """
    A simple endpoint for checking the status of the server.

    This is useful for monitoring the server, and for checking that the server is
    running correctly.
    """

    response = {
        "version": get_version(),
    }

    # Response with pong if ping is provided.
    ping = request.args.get("ping", None)
    if ping is not None:
        response["pong"] = f"{ping}"

    return jsonify(response)
