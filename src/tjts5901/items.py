from datetime import datetime, timedelta
import logging
from typing import Optional
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app
)
from werkzeug.exceptions import abort

from .auth import login_required, current_user
from .models import Bid, Item
from .notification import send_notification

bp = Blueprint('items', __name__)
api = Blueprint('api_items', __name__, url_prefix='/api/items')

logger = logging.getLogger(__name__)

from flask_babel import _, lazy_gettext
from markupsafe import Markup

MIN_BID_INCREMENT = 1

def get_item(id):
    """
    Returns an item.

    :param id: The ID of the item to be returned.
    :return: An item with the ID given as a parameter.
    """
    try:
        item = Item.objects.get_or_404(id=id)
    except Exception as exc:
        print("Error getting item:", exc)
        abort(404)

    #if item.seller == current_user:
    return item
    
    abort(403)

def get_winning_bid(item: Item) -> Optional[Bid]:
    """
    Return the (currently) winning bid for the given item.

    If there are no bids, return None.

    :param item: The item to get the winning bid for.
    :return: The winning bid, or None.
    """

    winning_bid = None

    # Return winning bid, if the item is closed
    if item.closed and item.winning_bid:
        return item.winning_bid

    # Sanity check: if the item is not closed, it should not have a winning bid
    assert not item.closed or not (not item.closed and winning_bid), "Item is not closed, but has a winning bid"

    try:
        winning_bid = Bid.objects(item=item) \
            .filter(created_at__lt=item.closes_at) \
            .order_by('-amount') \
            .first()
        # Print for debugging
        # print("Bid.objects:")
        # print(Bid.objects.first())
    except Exception as exc:
        logger.warning("Error getting winning bid: %s", exc, exc_info=True, extra={
            'item_id': item.id,
        })

    return winning_bid

def handle_item_closing(item):
    """
    Handle closing of an item.

    Checks if the item should be closed now and
    sends notification to the seller and the buyer

    :param item: Item to handle
    """
    # Handle the closing of an item
    if not item.is_open and not item.closed:
        logger.info("Closing item %r (%s)", item.title, item.id, extra={
            'item_id': item.id,
            'item_title': item.title,
            'item_closes_at': item.closes_at,
        })

        # Get the winning bid
        winning_bid = get_winning_bid(item)
        if winning_bid:
            item.winning_bid = winning_bid

            # Send a notifications to the seller and the buyer
            # lazy_gettext() is used to delay the translation until the message is sent
            # Markup.escape() is used to escape strings, to prevent XSS attacks
            send_notification(
                item.seller,
                title=lazy_gettext("Your item was sold"),
                message=lazy_gettext("Your item <em>%(title)s</em> was sold to %(buyer)s for %(price)s.",
                                     title=Markup.escape(item.title),
                                     buyer=Markup.escape(winning_bid.bidder.email),
                                     price=Markup.escape(winning_bid.amount)),
            )
            send_notification(
                winning_bid.bidder,
                title=lazy_gettext("You won an item"),
                message=lazy_gettext("You won the item <em>%(title)s</em> for %(price)s.",
                                     title=Markup.escape(item.title),
                                     price=Markup.escape(winning_bid.amount)),
            )

        else:
            # If there is no winning bid, send a notification to the seller
            send_notification(
                item.seller,
                title=lazy_gettext("Your item was not sold"),
                message=lazy_gettext("Your item <em>%(title)s</em> was not sold.",
                                     title=Markup.escape(item.title)),
            )

        # Close the item
        item.closed = True
        item.save()


def get_item_price(item: Item) -> int:
    """
    Return the current price of the given item.

    If there are no bids, return the starting bid.

    :param item: The item to get the price for.
    :return: The current price.
    """

    winning_bid = get_winning_bid(item)
    if winning_bid:
        return winning_bid.amount

    return item.starting_bid


@bp.route("/", methods=('GET', 'POST'))
@login_required
def index():
    """
    Shows all the items for sale in the same view.
    """
    if request.method == 'POST':
        bid_price = request.form['bid']
        id = request.form['itemId']

    items = Item.objects.all()
    #items.delete()
    
    return render_template('items/index.html',
        items=items)

@bp.route('/sell', methods=('GET', 'POST'))
@login_required
def sell():
    """
    Page where items can be put for sale.
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        starting_bid = int(float(request.form['starting_bid']))

        error = None

        if not title:
            error = _('Title is required.')
        if not starting_bid or starting_bid < 1:
            error = 'Starting bid must be greater than 0.'


        if error is None:
            try:
                sale_length = timedelta(days=1)
                # If debug mode is on, there will be option for quicker closing time for debugging.
                if current_app.config['DEBUG'] and request.form.get("flash-sale"):
                    sale_length = timedelta(seconds=60)

                item = Item(
                    title=title,
                    description=description,
                    starting_bid = starting_bid,
                    seller = current_user,
                    leading_bid = None,
                    closes_at = datetime.utcnow() + sale_length
                )
                item.save()
                return redirect(url_for('items.index'))
            except Exception as exc:
                error = _("Error creating item: %(exc)s", exc=exc)
                logger.warning("Error creating item: %s", exc, exc_info=True, extra={
                    'title': title,
                    'description': description,
                    'starting_bid': starting_bid,
                })

        else:
            print(error)
            flash(error, category='error')

    return render_template('items/sell.html')

@bp.route('/item/<id>', methods=('GET', 'POST'))
def view(id):
    """
    Item view page.

    Displays the item details, and a form to place a bid.
    """

    item = get_item(id)

    # Print item id for debugging
    print("Item ID: ")
    print(item.id)

    # Set the minimum price for the bid form from the current winning bid
    winning_bid = get_winning_bid(item)
    min_bid = get_item_price(item)

    # Print bids for debugging:
    # print("winning_bid:")
    # print(winning_bid)
    # print("winning_bid.amount: ")
    # print(winning_bid.amount)
    # print("min_bid:")
    # print(min_bid)

    # Inform the user if he/she has won the bid
    if winning_bid:
        if item.closes_at < datetime.utcnow():
            if winning_bid and winning_bid.bidder == current_user:
                flash(_("Congratulations! You won the auction!"), "success")
            else:
                flash(_("This item is no longer on sale."))

    return render_template('items/view.html', item=item, min_bid=min_bid)


@bp.route('/item/<id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    Item update page
    """

    item = get_item(id)

    print(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        error = None

        if not title:
            error = _('Title is required.')

        try:
            item.title = title
            item.description = description
            item.save()
        except Exception as exc:
            error = _("Error updating item: %(exc)s", exc=exc)
            logger.warning("Error updating item: %s", exc, exc_info=True, extra={
                'item_id': item.id,
            })
        else:
            flash(_("Item updated successfully!"))
            return redirect(url_for('items.index'))

        print(error)
        flash(error, category='error')


    return render_template('items/update.html', item=item)

@bp.route('/item/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    """
    Delete an item.
    """
    item = get_item(id)
    try:
        item.delete()
    except Exception as exc:
        logger.warning("Error deleting item: %s", exc, exc_info=True, extra={
            'item_id': item.id,
        })
        flash(_("Error deleting item: %(exc)s", exc=exc), category='error')
    else:
        flash("Item deleted successfully!")
    return redirect(url_for('items.index'))

@bp.route('/item/<id>/bid', methods=('POST',))
@login_required
def bid(id):
    """
    Bid on an item.

    If the bid is valid, create a new bid and redirect to the item view page.
    Otherwise, display an error message and redirect back to the item view page.

    :param id: The id of the item to bid on.
    :return: A redirect to the item view page.
    """

    item = Item.objects.get_or_404(id=id)
    min_amount = get_item_price(item)
    amount = int(request.form['amount'])

    #Bid must be higher than the last bid
    if amount <= min_amount:
        flash(f"Bid must be at least {min_amount+MIN_BID_INCREMENT}")
        return redirect(url_for('items.view', id=id))

    if item.closes_at < datetime.utcnow():
        flash("This item is no longer on sale.")
        return redirect(url_for('items.view', id=id))

    try:
        # Notice: if you have integrated the flask-login extension, use current_user
        # instead of g.user
        bid = Bid(
            item=item,
            bidder=current_user,
            amount=amount,
        )
        bid.save()
    except Exception as exc:
        flash(f"Error placing bid: {exc!s}")
    else:
        flash(_("Bid placed successfully!"))


    return redirect(url_for('items.view', id=id))


@api.route('<id>/bids', methods=('GET',))
@login_required
def api_item_bids(id):
    """
    Get the bids for an item.

    :param id: The id of the item to get bids for.
    :return: A JSON response containing the bids.
    """

    item = Item.objects.get_or_404(id=id)
    bids = []
    for bid in Bid.objects(item=item).order_by('-amount'):
        bids.append(bid.to_json())

    return jsonify({
        'success': True,
        'bids': bids
    })

@api.route('<id>/bids', methods=('POST',))
@login_required
def api_item_place_bid(id):
    """
    Place a bid on an item.

    If the bid is valid, create a new bid and return the bid.
    Otherwise, return an error message.
    
    Only accepts `REF_CURRENCY` bids.

    :param id: The id of the item to bid on.
    :return: A JSON response containing the bid.
    """

    item = Item.objects.get_or_404(id=id)
    min_amount = get_item_price(item)

    try:
        amount = int(request.form['amount'])
    except KeyError:
        return jsonify({
            'success': False,
            'error': _("Missing required argument %(argname)s", argname='amount')
        })
    except ValueError:
        return jsonify({
            'success': False,
            'error': _("Invalid value for argument %(argname)s", argname='amount')
        })
    except Exception as exc:
        return jsonify({
            'success': False,
            'error': _("Error parsing argument %(argname)s: %(exc)s", argname='amount', exc=exc)
        })

    if amount <= min_amount:
        return jsonify({
            'success': False,
            'error': _("Bid must be at least %(min_amount)s", min_amount=min_amount)
        })

    if item.closes_at < datetime.utcnow():
        return jsonify({
            'success': False,
            'error': _("This item is no longer on sale.")
        })

    try:
        bid = Bid(
            item=item,
            bidder=current_user,
            amount=amount,
        )
        bid.save()
    except Exception as exc:
        logger.error("Error placing bid: %s", exc, exc_info=True, extra={
            'item_id': item.id,
            'bidder_id': current_user.id,
            'amount': amount,
        })

        return jsonify({
            'success': False,
            'error': _("Error placing bid: %(exc)s", exc=exc)
        })

    return jsonify({
        'success': True,
        'bid': bid.to_mongo().to_dict()
    })