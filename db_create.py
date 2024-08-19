from acc_app import db, app
from acc_app.models.base_model import BaseModel
from acc_app.models.models import User, Item, Supplier, Customer, Purchase_invoice, Sales_invoice, purchase_item, sales_item

with app.app_context():
    db.create_all()
    print('Database created successfully')
