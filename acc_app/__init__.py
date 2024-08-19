from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config


# Create a Flask application
app = Flask(__name__)

# Load the Config class into the Flask app
app.config.from_object(Config)

# Create a database instance
db = SQLAlchemy(app)

# Create a Bcrypt instance
bcrypt = Bcrypt(app)

# Create a LoginManager instance
login_manager = LoginManager(app)
login_manager.login_view = 'user_bp.login'

#Import Routes
from acc_app.routes.main_routes import main_bp
from acc_app.routes.sales_routes import sales_bp
from acc_app.routes.purchase_routes import purchase_bp
from acc_app.routes.customers_routes import customer_bp
from acc_app.routes.item_routes import item_bp
from acc_app.routes.supplier_routes import supplier_bp
from acc_app.routes.investment_routes import investment_bp
from acc_app.routes.user_routes import user_bp

# Register the Blueprint
app.register_blueprint(main_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(item_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(investment_bp)
app.register_blueprint(user_bp)
