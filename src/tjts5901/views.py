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

    user = request.values.get("user")
    item = request.values.get("item")
    price = request.values.get("price")

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

    html = render_template("index.html.j2", items2=items2)
    return html

@bp.route("/test2", methods=['GET', 'POST'])
def index2() -> str:

    from .models import Item, User

    user = User()
    user.save()

    item = Item()
    item.title = "Test item 2"
    item.description = "This is a test item"
    item.starting_bid = 100
    item.seller = user
    item.save()

    return "OK!"