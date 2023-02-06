from datetime import datetime
from mongoengine import (
    StringField,
    IntField,
    ReferenceField,
    DateTimeField,
    EmailField,
)
from .db import db


class User(db.Document):
    """
    Model representing a user of the auction app.
    """

    email = EmailField(required=True, unique=True)
    "The user's email address."

    password = StringField(required=True)

    created_at = DateTimeField(required=True, default=datetime.utcnow)


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

    seller = ReferenceField(User, required=True)

    created_at = DateTimeField(required=True, default=datetime.utcnow)
    closes_at = DateTimeField()