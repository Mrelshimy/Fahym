from flask import Blueprint, render_template
from flask_login import current_user, login_required


supplier_bp = Blueprint('supplier_bp', __name__, url_prefix='/suppliers')


@supplier_bp.route('/')
@login_required
def get_suppliers():
    """ Render Sales Templates """
    return render_template('suppliers.html')


@supplier_bp.route('/add_supplier')
@login_required
def add_supplier():
    """ Add Sales Invoice """
    return render_template('add_supplier.html')
