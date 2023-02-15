from os import environ
import pytest
from tjts5901 import create_app

def pytest_addoption(parser: pytest.Parser):
    """
    Callback to add command-line options for pytest.

    Add option to define environment url to test.

    Usage example from agruments::
        $ pytest --environment-url "https://example.com"

    Note: GitLab CI automatically sets environment variable `CI_ENVIRONMENT_URL`
    to the address of environment to test.

    Usage example from environment variable::
        $ CI_ENVIRONMENT_URL="https://example.com" pytest

    Note: If you want to test locally, you can define environment variable in
    .env file.
    """

    parser.addoption("--environment-url",
                     dest="CI_ENVIRONMENT_URL",
                     help="Deployment webaddress",
                     default=environ.get("CI_ENVIRONMENT_URL"))


@pytest.fixture
def app():
    flask_app = create_app({
        'TESTING': True,
    })

    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
