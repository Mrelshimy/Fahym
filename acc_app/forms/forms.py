from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.validators import (DataRequired,
                                Email, EqualTo, Length, ValidationError)
from wtforms import (StringField,
                     PasswordField, EmailField, SubmitField, BooleanField)
from email_validator import validate_email, EmailNotValidError
from acc_app.models.models import User


class RegistrationForm(FlaskForm):
    """
    A form for registering new users.
    """
    email = EmailField("Email", validators=[DataRequired(), Email()])
    buss_name = StringField("Buss_name",
                            validators=[DataRequired(),
                                        Length(min=2, max=100)])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Confirm password",
                              validators=[DataRequired(),
                                          Length(min=6), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        try:
            v = validate_email(email.data, check_deliverability=False)
            email.data = v.normalized
        except EmailNotValidError as e:
            raise ValidationError(str(e))
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.\
                                  Please choose a different one.')

    def validate_buss_name(self, buss_name):
        user = User.query.filter_by(buss_name=buss_name.data).first()
        if user:
            raise ValidationError('That Business name is taken.\
                                  Please choose a different one.')


class LoginForm(FlaskForm):
    """
    A form for logging in users.
    """
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        """
        Validates the email field.

        args:
            email: The email to validate.

        returns:
            A validation error if the email is invalid.
        """
        u = User.query.filter_by(email=email.data).first()
        if u is None:
            raise ValidationError('There is no account with\
                                  that email. You must register first.')

    def validate_password(self, password):
        """ Validate password field """
        u = User.query.filter_by(email=self.email.data).first()
        if u is not None and not u.check_password(password.data):
            raise ValidationError('Password is incorrect.')


class RequestResetForm(FlaskForm):
    """
    A form for requesting a password reset.
    """
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        """
        Validates the email field.

        args:
            email: The email to validate.

        returns:
            A validation error if the email is invalid.
        """
        u = User.query.filter_by(email=email.data).first()
        if u is None:
            raise ValidationError('There is no account with\
                                  that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """
    A form for resetting a password.
    """
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Confirm password",
                              validators=[DataRequired(),
                                          Length(min=6), EqualTo('password')])
    submit = SubmitField('Reset Password')
