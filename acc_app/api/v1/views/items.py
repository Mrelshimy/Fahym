from flask import jsonify, abort, request
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import Item, sales_item, purchase_item
from sqlalchemy import desc
from uuid import uuid4


@views_bp.route('/items', methods=['GET'], strict_slashes=False)
def get_items():
    with app.app_context():
        items = db.session.query(Item).order_by(desc(Item.created_at)).all()
        data = [item.to_dict() for item in items]
        return jsonify(data), 200


@views_bp.route('/items/<item_id>', methods=['GET'], strict_slashes=False)
def get_item(item_id):
    with app.app_context():
        item = db.session.query(Item).get(item_id)
        if item is None:
            abort(404)
        return jsonify(item.to_dict()), 200


@views_bp.route('users/<user_id>/items', methods=['GET'], strict_slashes=False)
def get_user_items(user_id):
    with app.app_context():
        items = db.session.query(Item).filter_by(user_id=user_id)\
            .order_by(desc(Item.created_at)).all()
        data = [item.to_dict() for item in items]
        return jsonify(data), 200


@views_bp.route('users/<user_id>/items',
                methods=['POST'], strict_slashes=False)
def post_item(user_id):
    with app.app_context():
        if request.is_json:
            data = request.get_json()
            not_needed = ['id', 'created_at', 'updated_at']
            for value in not_needed:
                if value in data:
                    abort(400, 'id, created_at and updated_at are not needed')
            required = ['code', 'name', 'unit',
                        'purchase_price', 'sales_price']
            for value in required:
                if value not in data:
                    abort(400, f'{value} is required')
            data['user_id'] = user_id
            id = uuid4()
            item = Item(id=id, **data)
            db.session.add(item)
            db.session.commit()
            return jsonify({"message": "Item added successfully"}), 200
        else:
            abort(400, 'Not a JSON')


@views_bp.route('/items/<item_id>',
                methods=['DELETE'], strict_slashes=False)
def delete_item(item_id):
    with app.app_context():
        item = db.session.query(Item).get(item_id)
        if item is None:
            abort(404)
        sales_references = db.session.query(sales_item)\
            .filter_by(item_id=item.id).count()
        purchase_references = db.session.query(purchase_item)\
            .filter_by(item_id=item.id).count()
        if sales_references > 0 or purchase_references > 0:
            abort(400, 'Item is referenced in sales or purchase invoices')
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"}), 200


@views_bp.route('/items/<item_id>',
                methods=['PUT'], strict_slashes=False)
def update_item(item_id):
    with app.app_context():
        item = db.session.query(Item).get(item_id)
        if item is None:
            abort(404)
        if request.is_json:
            data = request.get_json()
            not_required = ['id', 'created_at', 'updated_at', 'user_id']
            for key, value in data.items():
                if key in not_required:
                    continue
                else:
                    setattr(item, key, value)
            Item.save(item)
            db.session.commit()
            return jsonify({"message": "Item updated successfully"}), 200
        else:
            abort(400, 'Not a JSON')
