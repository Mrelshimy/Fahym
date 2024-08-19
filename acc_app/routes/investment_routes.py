from flask import Blueprint, render_template
from flask_login import current_user, login_required


investment_bp = Blueprint('investment_bp', __name__, url_prefix='/investments')


@investment_bp.route('/')
@login_required
def get_investments():
    """ Render Sales Templates """
    return render_template('investments.html')


@investment_bp.route('/add_investment')
@login_required
def add_investment():
    """ Add Sales Invoice """
    return render_template('add_investment.html')
