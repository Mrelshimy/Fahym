import os


# Create a Config class
class Config:
    """
    Set the configuration variables for the Flask application
    """
    SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ["DB_USER"]}:\
{os.environ["DB_PASS"]}\
@{os.environ["DB_HOST"]}/{os.environ["DB_NAME"]}'
    SECRET_KEY = os.urandom(32)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'mraafat.elsayed@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
