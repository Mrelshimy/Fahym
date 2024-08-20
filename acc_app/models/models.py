from acc_app.models.base_model import BaseModel
from acc_app import db, app, bcrypt, login_manager, secret_key
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import uuid
import jwt


# login manager
@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by its id.

    Returns:
        The user with the given id.
    """
    return db.session.query(User).get(user_id)


purchase_item = db.Table('purchase_item',
                         db.Column('id',
                                   db.String(36),
                                   primary_key=True, default=uuid.uuid4()),
                         db.Column('created_at',
                                   db.DateTime,
                                   nullable=False, default=datetime.now()),
                         db.Column('updated_at',
                                   db.DateTime,
                                   nullable=False, default=datetime.now()),
                         db.Column('item_id',
                                   db.String(36),
                                   db.ForeignKey('item.id')),
                         db.Column('purchase_invoice_id',
                                   db.String(36),
                                   db.ForeignKey('purchase_invoice.id')),
                         db.Column('item_quantity',
                                   db.Float,
                                   nullable=False, default=1),
                         db.Column('item_price',
                                   db.Float, nullable=False))


sales_item = db.Table('sales_item',
                      db.Column('id',
                                db.String(36),
                                primary_key=True, default=uuid.uuid4()),
                      db.Column('created_at',
                                db.DateTime,
                                nullable=False, default=datetime.now()),
                      db.Column('updated_at',
                                db.DateTime,
                                nullable=False, default=datetime.now()),
                      db.Column('item_id',
                                db.String(36),
                                db.ForeignKey('item.id')),
                      db.Column('sales_invoice_id',
                                db.String(36),
                                db.ForeignKey('sales_invoice.id')),
                      db.Column('item_quantity',
                                db.Float,
                                nullable=False, default=1),
                      db.Column('item_price',
                                db.Float, nullable=False))


class User(BaseModel, UserMixin, SerializerMixin):
    """
    User model class
    """
    buss_name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    buss_logo = db.Column(db.String(255),
                          nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    items = db.relationship('Item', backref='user',
                            lazy=True, cascade='all, delete')
    suppliers = db.relationship('Supplier', backref='user',
                                lazy=True, cascade='all, delete')
    customers = db.relationship('Customer', backref='user',
                                lazy=True, cascade='all, delete')
    pur_invoices = db.relationship('Purchase_invoice', backref='user',
                                   lazy=True, cascade='all, delete')
    sales_invoices = db.relationship('Sales_invoice', backref='user',
                                     lazy=True, cascade='all, delete')
    investments = db.relationship('Investment', backref='user',
                                  lazy=True, cascade='all, delete')

    serialize_rules = ('-password')

    def set_password(self, password):
        """
        Sets the user's password.

        Returns:
            The user's password hashed inside database.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, passwd):
        """
        Checks the user's password.
        """
        return bcrypt.check_password_hash(self.password, passwd)

    def get_token(self):
        """
        Generates a token for the user.

        Returns:
            A token for the user.
        """
        encoded_user_id = jwt.encode({'user_id': self.id},
                                     secret_key, algorithm='HS256')
        return encoded_user_id

    def __repr__(self):
        return f"User('{self.buss_name}')"


class Item(BaseModel, UserMixin):
    """
    Item model class
    """
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    purchase_price = db.Column(db.Float, nullable=False, default=0)
    sales_price = db.Column(db.Float, nullable=False, default=0)
    stock = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(10), nullable=False)
    attachment = db.Column(db.String(255))
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.code}, {self.name}')"


class Supplier(BaseModel, UserMixin):
    """
    Supplier model class
    """
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Supplier('{self.name}, {self.code}')"


class Customer(BaseModel, UserMixin):
    """
    Customer model class
    """
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Customer('{self.name}, {self.code}')"


class Purchase_invoice(BaseModel, UserMixin):
    """
    Purchase invoice model class
    """
    code = db.Column(db.String(20), nullable=False, unique=True)
    landed_cost = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False)
    remarks = db.Column(db.Text)
    attachment = db.Column(db.String(255))
    total_price = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.String(36),
                            db.ForeignKey('supplier.id'), nullable=False)
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Item', secondary=purchase_item,
                            backref='purchase_invoices',
                            lazy=True, cascade='all, delete')

    def __repr__(self):
        return f"Purchase_Invoice('{self.code}')"


class Sales_invoice(BaseModel, UserMixin):
    """
    Sales invoice model class
    """
    code = db.Column(db.String(20), nullable=False, unique=True)
    shipping_cost = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False)
    remarks = db.Column(db.Text)
    attachment = db.Column(db.String(255))
    total_price = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.String(36),
                            db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id'), nullable=False)

    items = db.relationship('Item', secondary=sales_item,
                            backref='sales_invoices',
                            lazy=True, cascade='all, delete')

    def __repr__(self):
        return f"Sales_Invoice('{self.code}')"


class Investment(BaseModel, UserMixin):
    """
    Investment model class
    """
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.Text)
    attachment = db.Column(db.String(255))
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Investment('{self.code}')"
