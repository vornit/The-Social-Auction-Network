"""
Basic views for Application
===========================
"""

from flask import Blueprint, render_template, send_from_directory
from flask import Flask, session, redirect, url_for, escape, request, Response, Markup, make_response
import json
import urllib

# Main blueprint.
bp = Blueprint('views', __name__)

# Blueprint for documentation.
docs_bp = Blueprint('docs', __name__)

@bp.route("/", methods=['GET', 'POST'])
def index() -> str:

    user_input = request.values.get("user")
    item_input = request.values.get("item")
    price_input = request.values.get("price")

    from .models import Item, User

    item_adding_text = ""

    try:
        user = User()
        user.save()

        item = Item()
        item.title = item_input
        item.description = "No desc yet"
        item.starting_bid = price_input
        item.seller = user
        item.save()
        item_adding_text = "Item added successfully!"
    except:
        item_adding_text = "Failed to add item!"
    

    try:
        if (user != "" and item != "" and price != ""):
            file = open("items.txt", "a")
            file.write("\n" + user + ", " + item + ", " + price + "€")
            file.close()
    except:
        pass

    try:
        file = open("items.txt", "r")
        items = file.read().split("\n")
        items2 = []
        for i in items:
            items2.append(i.split(','))
    except:
        items = ""

    html = render_template("index.html.j2", items2=items2, item_adding_text=item_adding_text)
    return html

#@bp.route("/test2", methods=['GET', 'POST'])
#def index2() -> str:
#
#    from .models import Item, User
#
#    user = User()
#    user.save()
#
#    item = Item()
#    item.title = "Test item 2"
#    item.description = "This is a test item"
#    item.starting_bid = 100
#    item.seller = user
#    item.save()
#
#    return "OK!"