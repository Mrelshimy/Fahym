from flask import Blueprint, render_template


main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def index():
    """ Render Homepage """
    return render_template('homepage.html')
