from flask import Blueprint


# Create a Blueprint for the api views
views_bp = Blueprint('views', __name__, url_prefix='/acc_app/api/v1')


from acc_app.api.v1.views.users import *
from acc_app.api.v1.views.items import *
from acc_app.api.v1.views.purchase_invoices import *
from acc_app.api.v1.views.sales_invoices import *
from acc_app.api.v1.views.suppliers import *
from acc_app.api.v1.views.customers import *
from acc_app.api.v1.views.investments import *
from acc_app.api.v1.views.sales_items import *
