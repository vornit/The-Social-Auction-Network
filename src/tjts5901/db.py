from os import environ
from flask_mongoengine import MongoEngine

db = MongoEngine()

def init_db(app) -> None:
    """
    Initialize connection to database
    """

    mongodb_url = environ.get("MONGODB_URL")
    if mongodb_url is not None:
        app.config["MONGODB_SETTINGS"] = {
            "host": mongodb_url,
        }

    db.init_app(app)