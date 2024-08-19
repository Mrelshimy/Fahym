from flask import Blueprint, render_template
from flask_login import current_user, login_required


item_bp = Blueprint('item_bp', __name__, url_prefix='/items')


@item_bp.route('/')
@login_required
def get_items():
    """ Render Sales Templates """
    return render_template('items.html')


@item_bp.route('/add_item')
@login_required
def add_item():
    """ Add Sales Invoice """
    return render_template('add_item.html')
