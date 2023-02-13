from datetime import datetime
from secrets import token_urlsafe

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

    created_at = DateTimeField(required=True, default=datetime.utcnow())
    closes_at = DateTimeField()

    @property
    def is_open(self) -> bool:
        """
        Return whether the item is open for bidding.
        """
        return self.closes_at > datetime.utcnow()

class Bid(db.Document):
    """
    A model for bids on items.
    """

    amount = IntField(required=True, min_value=0)
    "Indicates the value of the bid."

    bidder = ReferenceField(User, required=True)
    "User who placed the bid."

    item = ReferenceField(Item, required=True)
    "Item that the bid is for."

    created_at = DateTimeField(required=True, default=datetime.utcnow)
    "Date and time that the bid was placed."


class AccessToken(db.Document):
    """
    Access token for a user.

    This is used to authenticate API requests.
    """

    meta = {"indexes": [
        {"fields": [
            "token",
            "user",
            "expires",
        ]}
    ]}

    name = StringField(max_length=100, required=True)
    "Human-readable name for the token."

    user = ReferenceField(User, required=True)
    "User that the token is for."

    token = StringField(required=True, unique=True, default=token_urlsafe)
    "The token string."

    last_used_at = DateTimeField(required=False)
    "Date and time that the token was last used."

    created_at = DateTimeField(required=True, default=datetime.utcnow)
    "Date and time that the token was created."

    expires = DateTimeField(required=False)
    "Date and time that the token expires."