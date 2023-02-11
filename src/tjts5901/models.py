from datetime import datetime
from mongoengine import (
    StringField,
    IntField,
    ReferenceField,
    DateTimeField,
    EmailField,
    BooleanField,
)
from .db import db
from flask_login import UserMixin
from bson import ObjectId


class User(UserMixin, db.Document):
    """
    Model representing a user of the auction app.
    """
    id: ObjectId
    "Id given to the user"

    email = EmailField(unique=True)
    "The user's email address."

    password = StringField()

    created_at = DateTimeField(required=True, default=datetime.utcnow)

    is_disabled = BooleanField(default=False)
    "Whether the user is disabled, banned in practical terms"

    @property
    def is_active(self) -> bool:
        """
        Return whether the user is active.

        This is used by Flask-Login to determine whether the user is
        allowed to log in.
        """
        return not self.is_disabled

    def get_id(self) -> str:
        """
        Return the user's id as a string.
        """
        return str(self.id)


class Item(db.Document):
    """
    Model representing an item in the auction.
    """

    # Create index for sorting items by closing time, as Azure MondoDB does not do it automatically
    meta = {"indexes": [
        {"fields": [
            "closes_at",
        ]}
    ]}

    title = StringField(min_length=1, max_length=70, required=True)
    description = StringField(max_length=1500, required=True)

    starting_bid = IntField(required=True, min_value=0)

    leading_bid = StringField(max_length=100)

    seller = ReferenceField(User, required=True)

    created_at = DateTimeField(required=True, default=datetime.utcnow)
    closes_at = DateTimeField()