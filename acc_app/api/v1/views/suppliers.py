from flask import jsonify, abort, request
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import Supplier
from sqlalchemy import desc
from uuid import uuid4


@views_bp.route('/suppliers',
                methods=['GET'], strict_slashes=False)
def get_suppliers():
    with app.app_context():
        suppliers = db.session.query(Supplier)\
            .order_by(desc(Supplier.created_at)).all()
        data = [supplier.to_dict() for supplier in suppliers]
        return jsonify(data), 200


@views_bp.route('/suppliers/<supplier_id>',
                methods=['GET'], strict_slashes=False)
def get_supplier(supplier_id):
    with app.app_context():
        supplier = db.session.query(Supplier).get(supplier_id)
        if supplier is None:
            abort(404)
        return jsonify(supplier.to_dict()), 200


@views_bp.route('/users/<user_id>/suppliers',
                methods=['GET'], strict_slashes=False)
def get_user_suppliers(user_id):
    with app.app_context():
        suppliers = db.session.query(Supplier)\
            .filter_by(user_id=user_id)\
            .order_by(desc(Supplier.created_at)).all()
        data = [supplier.to_dict() for supplier in suppliers]
        return jsonify(data), 200


@views_bp.route('/users/<user_id>/suppliers',
                methods=['POST'], strict_slashes=False)
def post_supplier(user_id):
    with app.app_context():
        if request.is_json:
            data = request.get_json()
            not_needed = ['id', 'created_at', 'updated_at']
            for value in not_needed:
                if value in data:
                    abort(400, 'id, created_at and updated_at are not needed')
            required = ['code', 'name']
            for value in required:
                if value not in data:
                    abort(400, f'{value} is required')
            data['user_id'] = user_id
            id = uuid4()
            supplier = Supplier(id=id, **data)
            db.session.add(supplier)
            db.session.commit()
            return jsonify({"message": "Supplier added"}), 200
        else:
            abort(400, 'Not a JSON')


@views_bp.route('/suppliers/<supplier_id>',
                methods=['DELETE'], strict_slashes=False)
def delete_supplier(supplier_id):
    with app.app_context():
        supplier = db.session.query(Supplier).get(supplier_id)
        if supplier is None:
            abort(404)
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({"message": "supplier deleted successfully"}), 200


@views_bp.route('/suppliers/<supplier_id>',
                methods=['PUT'], strict_slashes=False)
def update_supplier(supplier_id):
    with app.app_context():
        supplier = db.session.query(Supplier).get(supplier_id)
        if supplier is None:
            abort(404)
        if request.is_json:
            data = request.get_json()
            not_required = ['id', 'created_at', 'updated_at', 'user_id']
            for key, value in data.items():
                if key in not_required:
                    continue
                else:
                    setattr(supplier, key, value)
            Supplier.save(supplier)
            db.session.commit()
            return jsonify({"message": "supplier updated"}), 200
        else:
            abort(400, 'Not a JSON')
