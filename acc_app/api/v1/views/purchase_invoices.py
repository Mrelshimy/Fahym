from flask import jsonify, abort, request
from sqlalchemy import desc
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import Purchase_invoice, Supplier, Item, purchase_item
from uuid import uuid4
from datetime import datetime

@views_bp.route('/purchase_invoices', methods=['GET'], strict_slashes=False)
def get_purchase_invoices():
    with app.app_context():
        invoices = db.session.query(Purchase_invoice).order_by(desc(Purchase_invoice.created_at)).all()
        data = [purchase_invoice.to_dict() for purchase_invoice in invoices]
        return jsonify(data), 200


@views_bp.route('/purchase_invoices/<invoice_id>', methods=['GET'], strict_slashes=False)
def get_pur_invoice(invoice_id):
    with app.app_context():
        invoice = db.session.query(Purchase_invoice).get(invoice_id)
        if invoice is None:
            abort(404)
        return jsonify(invoice.to_dict()), 200


@views_bp.route('users/<user_id>/purchase_invoices', methods=['GET'], strict_slashes=False)
def get_user_purchase_invoices(user_id):
    with app.app_context():
        invoices = db.session.query(Purchase_invoice).filter_by(user_id=user_id).order_by(desc(Purchase_invoice.created_at)).all()
        data = [purchase_invoice.to_dict() for purchase_invoice in invoices]
        return jsonify(data), 200


@views_bp.route('/users/<user_id>/purchase_invoices', methods=['POST'], strict_slashes=False)
def post_pur_invoice(user_id):
    with app.app_context():
        if request.is_json:
            data = request.get_json()
            not_required = ['id', 'created_at', 'updated_at']
            for value in not_required:
                if value in data:
                    abort(400, f'{value} is not required')
            required = ['total_price', 'code', 'supplier', 'items', 'date']
            for value in required:
                if value not in data:
                    abort(400, f'{value} is required')
            supplier = db.session.query(Supplier).filter_by(name=data['supplier']).one()
            del(data['supplier'])
            data['supplier_id'] = supplier.id       
            data['user_id'] = user_id
            data['id'] = str(uuid4())
            items = data['items']
            del(data['items'])
            
            purchase_invoice = Purchase_invoice(**data)
            db.session.add(purchase_invoice)
            for item in items:
                get_item = db.session.query(Item).filter_by(code=item['item']).one()
                purchase_item_entry = purchase_item.insert().values(
                    id=str(uuid4()),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    purchase_invoice_id=purchase_invoice.id,
                    item_id=get_item.id,
                    item_quantity=item['quantity'],
                    item_price=item['price'])
                db.session.execute(purchase_item_entry)
                get_item.stock += float(item['quantity'])
            
            db.session.commit()
            return jsonify({"message": "Invoice added successfully"}), 200
        else:
            abort(400, 'Not a JSON')


@views_bp.route('/purchase_invoices/<invoice_id>', methods=['DELETE'], strict_slashes=False)
def delete_pur_invoice(invoice_id):
    with app.app_context():
        invoice = db.session.query(Purchase_invoice).get(invoice_id)
        if invoice is None:
            abort(404)
        db.session.execute(purchase_item.delete().where(purchase_item.c.purchase_invoice_id == invoice.id))
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({"message": "Invoice deleted successfully"}), 200


@views_bp.route('/purchase_invoices/<invoice_id>', methods=['PUT'], strict_slashes=False)
def update_pur_invoice(invoice_id):
    with app.app_context():
        invoice = db.session.query(Purchase_invoice).get(invoice_id)
        if invoice is None:
            abort(404)
        if request.is_json:
            data = request.get_json()
            for key, value in data.items():
                if key == "created_at" or\
                    key == "updated_at" or\
                        key == 'user_id' or\
                            key == "id":
                    continue
                else:
                    setattr(invoice, key, value)
            Purchase_invoice.save(invoice)
            db.session.commit()
            return jsonify({"message": "Invoice updated successfully"}), 200
        else:
            abort(400, 'Not a JSON')
