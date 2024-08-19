from flask import render_template, redirect, url_for, request, Blueprint, flash
from acc_app.forms.forms import RegistrationForm, LoginForm
from acc_app.models.models import User
from acc_app import app, db
from flask_login import current_user, login_user, logout_user, login_required


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.is_authenticated:
        return render_template('admin_panel.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in a user.

    Returns:
        A rendered template for the login.html page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('user_bp.admin_panel'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('user_bp.admin_panel'))
    return render_template('login.html', form=form)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_bp.admin_panel'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    buss_name=form.buss_name.data)
        user.set_password(user.password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_bp.admin_panel'))

    return render_template('register.html', form=form)


@user_bp.route('/logout')
@login_required
def logout():
    """
    Logs out a user.

    Returns:
        A redirect to the home page.
    """
    logout_user()
    return redirect(url_for('main_bp.index'))
