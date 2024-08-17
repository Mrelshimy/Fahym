from flask import jsonify, abort, request
from sqlalchemy import desc
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import Sales_invoice, Customer, Item, sales_item
from uuid import uuid4
from datetime import datetime


@views_bp.route('/sales_invoices', methods=['GET'], strict_slashes=False)
def get_sales_invoices():
    """
    Get all sales invoices
    """
    with app.app_context():
        invoices = db.session.query(Sales_invoice)\
            .order_by(desc(Sales_invoice.created_at)).all()
        data = [sales_invoice.to_dict() for sales_invoice in invoices]
        return jsonify(data), 200


@views_bp.route('/sales_invoices/<invoice_id>',
                methods=['GET'], strict_slashes=False)
def get_sales_invoice(invoice_id):
    """
    Get a single sales invoice
    """
    with app.app_context():
        invoice = db.session.query(Sales_invoice).get(invoice_id)
        if invoice is None:
            abort(404)
        return jsonify(invoice.to_dict()), 200


@views_bp.route('users/<user_id>/sales_invoices',
                methods=['GET'], strict_slashes=False)
def get_user_sales_invoices(user_id):
    """
    Get all sales invoices for a user
    """
    with app.app_context():
        invoices = db.session.query(Sales_invoice)\
            .filter_by(user_id=user_id)\
            .order_by(desc(Sales_invoice.created_at)).all()
        data = [sales_invoice.to_dict() for sales_invoice in invoices]
        return jsonify(data), 200


@views_bp.route('/users/<user_id>/sales_invoices',
                methods=['POST'], strict_slashes=False)
def post_sales_invoice(user_id):
    """
    Add a sales invoice
    """
    with app.app_context():
        if request.is_json:
            data = request.get_json()
            not_required = ['id', 'created_at', 'updated_at']
            for value in not_required:
                if value in data:
                    abort(400, f'{value} is not required')
            required = ['total_price', 'code', 'customer', 'items', 'date']
            for value in required:
                if value not in data:
                    abort(400, f'{value} is required')
            customer = db.session.query(Customer)\
                .filter_by(name=data['customer']).one()
            del(data['customer'])
            data['customer_id'] = customer.id
            data['user_id'] = user_id
            data['id'] = str(uuid4())
            items = data['items']
            del(data['items'])
            sales_invoice = Sales_invoice(**data)
            db.session.add(sales_invoice)
            for item in items:
                get_item = db.session.query(Item)\
                    .filter_by(code=item['item']).one()
                sales_item_entry = sales_item.insert().values(
                    id=str(uuid4()),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    sales_invoice_id=sales_invoice.id,
                    item_id=get_item.id,
                    item_quantity=item['quantity'],
                    item_price=item['price'])
                db.session.execute(sales_item_entry)
                get_item.stock -= float(item['quantity'])
            db.session.commit()
            return jsonify({"message": "Invoice added successfully"}), 200
        else:
            abort(400, 'Not a JSON')


@views_bp.route('/sales_invoices/<invoice_id>',
                methods=['DELETE'], strict_slashes=False)
def delete_sales_invoice(invoice_id):
    """
    Delete a sales invoice
    """
    with app.app_context():
        invoice = db.session.query(Sales_invoice).get(invoice_id)
        if invoice is None:
            abort(404)
        db.session.execute(sales_item.delete()
                           .where(sales_item.c.sales_invoice_id
                                  == invoice.id))
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({"message": "Invoice deleted successfully"}), 200


@views_bp.route('/sales_invoices/<invoice_id>',
                methods=['PUT'], strict_slashes=False)
def update_sales_invoice(invoice_id):
    """
    Update a sales invoice
    """
    with app.app_context():
        invoice = db.session.query(Sales_invoice).get(invoice_id)
        if invoice is None:
            abort(404)
        if request.is_json:
            data = request.get_json()
            not_required = ['id', 'created_at', 'updated_at', 'user_id']
            for key, value in data.items():
                if key in not_required:
                    continue
                else:
                    setattr(invoice, key, value)
            Sales_invoice.save(invoice)
            db.session.commit()
            return jsonify({"message": "Invoice updated successfully"}), 200
        else:
            abort(400, 'Not a JSON')
