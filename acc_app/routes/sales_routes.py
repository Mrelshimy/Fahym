from flask import Blueprint, render_template
from flask_login import current_user, login_required


sales_bp = Blueprint('sales_bp', __name__, url_prefix='/sales')


@sales_bp.route('/')
@login_required
def get_sales():
    """ Render Sales Templates """
    return render_template('sales.html')


@sales_bp.route('/add_sales')
@login_required
def add_sales():
    """ Add Sales Invoice """
    return render_template('add_sales.html')
