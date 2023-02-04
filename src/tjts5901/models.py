from .db import db
from datetime import datetime
from mongoengine import (
    DateTimeField,
    EmailField,
    StringField,
)

class User(db.Document):
    """
    Class for userprofiles.
    Userprofile needs a email and a password.
    Date and time when the profile was created will be saved.
    """
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)