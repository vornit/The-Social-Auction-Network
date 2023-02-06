"""
Logging module
==============

This module provides a logging class that can be used to log messages
"""

import logging
from flask import Flask
from flask.logging import default_handler as flask_handler

# Set up logger instance to get access to the logger outside of module
logger = logging.getLogger("tjts5901")

def init_logging(app: Flask):
    """
    Integrates logging interface into the application.

    To bind logger into an application instance use::
        >>> init_logging(app)

    :param app: :class:`~Flask` The Flask application instance
    """
    
    # If the application is in debug mode, we want to log everything including debug messages
    if app.config.get("DEBUG"):
        logger.setLevel(level=logging.DEBUG)

    # Add flask's default handler to the logger. Whenever the flask logging handler is changed, this will be updated
    # as well
    logger.addHandler(flask_handler)

    logger.debug("TJTS5901 Logger initialized.")