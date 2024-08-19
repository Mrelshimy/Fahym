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
                           validators=[DataRequired(), Length(min=2, max=100)])
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
