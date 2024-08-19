from flask import Blueprint, render_template
from flask_login import current_user, login_required


purchase_bp = Blueprint('purchase_bp', __name__, url_prefix='/purchases')


@purchase_bp.route('/')
@login_required
def get_purchases():
    """ Render Sales Templates """
    return render_template('purchases.html')


@purchase_bp.route('/add_purchase')
@login_required
def add_purchas():
    """ Add Sales Invoice """
    return render_template('add_purchase.html')
