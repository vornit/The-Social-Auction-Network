"""
Main entry point for the application.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This file is used to run the application in development mode.

To run the application in development mode, run the following command:

    python -m tjts5901

"""

from os import environ
from .app import app

if __name__ == "__main__":
    port = int(environ.get("PORT", "5001"))
    host = environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port, debug=True)
