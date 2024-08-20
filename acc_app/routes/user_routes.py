from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_mail import Message
from acc_app.forms.forms import (RegistrationForm, LoginForm,
                                 RequestResetForm, ResetPasswordForm)
from acc_app.models.models import User
from acc_app import app, db, mail, secret_key
from flask_login import current_user, login_user, logout_user, login_required
import jwt


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


def send_reset_email(user):
    """
    Sends a password reset email to the user.

    Args:
        user: The user to send the email to.
    """
    token = user.get_token()
    reset_url = url_for('user_bp.reset_request', _external=True)
    reset_url_with_token = reset_url + f"/{token}"
    msg = Message('Password Reset Request', sender='noreply@fahym.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{reset_url_with_token}

If you didn't make this request, ignore this email.
'''
    mail.send(msg)


@user_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """
    Requests a password reset.

    Returns:
        A rendered template for the reset_request.html page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent\
              with instructions to reset your password')
        return redirect(url_for('main_bp.index'))
    return render_template('reset_request.html', form=form)


@user_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    Resets a password.

    Args:
        token: The token to reset the password.

    Returns:
        A rendered template for the reset_token.html page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    user_id = jwt.decode(token, secret_key, algorithms=['HS256'])['user_id']
    user = User.query.get(user_id)
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('users_bp.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('user_bp.login'))
    return render_template('reset_token.html', form=form)
