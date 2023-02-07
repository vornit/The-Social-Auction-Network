"""
Logging module
==============

This module provides a logging class that can be used to log messages
"""

import logging
from os import environ

import sentry_sdk
from flask import Flask
from flask.logging import default_handler as flask_handler
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.pymongo import PyMongoIntegration


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

    # Add flask's default handler to the logger. Whenever the flask logging handler is changed, 
    # this will be updated as well.
    logger.addHandler(flask_handler)

    logger.debug("TJTS5901 Logger initialized.")

    # Populate config with environment variables for sentry logging
    app.config.setdefault("SENTRY_DSN", environ.get("SENTRY_DSN"))
    app.config.setdefault("CI_COMMIT_SHA", environ.get("CI_COMMIT_SHA"))
    app.config.setdefault("CI_ENVIRONMENT_NAME", environ.get("CI_ENVIRONMENT_NAME"))

    # Set up sentry logging
    sentry_dsn = app.config.get("SENTRY_DSN")
    release = app.config.get("CI_COMMIT_SHA")

    # Try to get environment name from different sources
    if environment := app.config.get("CI_ENVIRONMENT_NAME"):
        environment = environment.lower()
    elif app.testing:
        environment = "testing"
    elif app.debug:
        environment = "development"

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration(), PyMongoIntegration()],

            # Capture 100% of transactions for performance monitoring. Might have to be adjusted for production.
            traces_sample_rate=1.0,

            release=release,
            environment=environment,
        )
    else:
        logger.warning("Sentry DSN not found. Logging to Sentry will be disabled.")
