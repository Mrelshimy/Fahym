from flask import Blueprint, render_template
from flask_login import current_user, login_required


main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def index():
    """ Render Dashboard """
    return render_template('homepage.html')
