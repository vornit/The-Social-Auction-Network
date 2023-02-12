from datetime import datetime, timedelta
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required, current_user
from .models import Item, User

bp = Blueprint('items', __name__)


def get_item(id):
    try:
        item = Item.objects.get_or_404(id=id)
    except Exception as exc:
        print("Error getting item:", exc)
        abort(404)

    #if item.seller == current_user:
    return item
    
    abort(403)


def bid_on_item(id, bid_price):
        print(bid_price)
        print(id)

        item = get_item(id)

        item.starting_bid = bid_price
        item.leading_bid = current_user.email
        item.save()


@bp.route("/", methods=('GET', 'POST'))
@login_required
def index():

    if request.method == 'POST':
        bid_price = request.form['bid']
        id = request.form['itemId']
        bid_on_item(id, bid_price)

    items = Item.objects.all()
    #items.delete()

    
    return render_template('items/index.html',
        items=items)

@bp.route('/sell', methods=('GET', 'POST'))
@login_required
def sell():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        starting_bid = int(request.form['starting_bid'])


        error = None

        if not title:
            error = 'Title is required.'
        if not starting_bid or starting_bid < 1:
            error = 'Starting bid must be greater than 0.'


        if error is None:
            try:
                item = Item(
                    title=title,
                    description=description,
                    starting_bid = starting_bid,
                    seller = current_user,
                    leading_bid = None,
                    closes_at = datetime.utcnow() + timedelta(days=1)
                )
                item.save()
            except Exception as exc:
                error = f"Error creating item: {exc!s}"

            else:
                return redirect(url_for('items.index'))

            print(error)
            flash(error)
        
            return redirect(url_for('items.index'))

    return render_template('items/sell.html')

# Allow the user to view the item in detail, bid on it and share on social media
@bp.route('/item/<id>/view', methods=('GET', 'POST'))
@login_required
def view(id):

    item = get_item(id)

    if request.method == 'POST':
        id = request.form['itemId']
        bid = request.form['bid']
        bid_on_item(id, bid)

    print(id)

    return render_template('items/view.html', item=item)

@bp.route('/item/<id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    item = get_item(id)

    print(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        try:
            item.title = title
            item.description = description
            item.save()
        except Exception as exc:
            error = f"Error updating item: {exc!s}"
        else:
            flash("Item updated successfully!")
            return redirect(url_for('items.index'))

        print(error)
        flash(error)

    return render_template('items/update.html', item=item)

@bp.route('/item/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    item = get_item(id)
    try:
        item.delete()
    except Exception as exc:
        error = f"Error deleting item: {exc!s}"
        print(error)
        flash(error)
    else:
        flash("Item deleted successfully!")
    return redirect(url_for('items.index'))