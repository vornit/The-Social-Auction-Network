"""
Module entry point.

Note: This file is only used when running the application directly. When app started
from Flask or gunicorn, this file is skipped.

To run the application module using this file, run the following command:
    python -m tjts5901

"""

from os import environ
from .app import app

if __name__ == "__main__":
    port = int(environ.get("PORT", "5001"))
    host = environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port, debug=True)
