from os import environ
from importlib.metadata import version, PackageNotFoundError


def get_version() -> str:
    """
    Get the version of the application.

    This is useful for checking the version of the application, and for
    monitoring the application.
    """

    # Get the version from the environment varible. It's setup by CI/CD pipeline.
    ver = environ.get("CI_COMMIT_SHA", None)

    if ver is None:
        try:
            # Get the version from the package.
            ver = version('tjts5901')
        except PackageNotFoundError:
            # Package is not installed.
            ver = "0.0.0-dev"

    return str(ver)
