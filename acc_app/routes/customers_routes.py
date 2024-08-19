from flask import Blueprint, render_template
from flask_login import current_user, login_required


customer_bp = Blueprint('customer_bp', __name__, url_prefix='/customers')


@customer_bp.route('/')
@login_required
def get_sales():
    """ Render Sales Templates """
    return render_template('customers.html')


@customer_bp.route('/add_customer')
@login_required
def add_sales():
    """ Add Sales Invoice """
    return render_template('add_customer.html')
