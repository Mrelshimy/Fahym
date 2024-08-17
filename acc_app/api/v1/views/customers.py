from flask import jsonify, abort, request
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import Customer
from sqlalchemy import desc
from uuid import uuid4


@views_bp.route('/customers', methods=['GET'], strict_slashes=False)
def get_customers():
    """
    Get all customers
    """
    with app.app_context():
        customers = db.session.query(Customer)\
            .order_by(desc(Customer.created_at)).all()
        data = [customer.to_dict() for customer in customers]
        return jsonify(data), 200


@views_bp.route('/customers/<customer_id>',
                methods=['GET'], strict_slashes=False)
def get_customer(customer_id):
    """
    Get a single customer
    """
    with app.app_context():
        customer = db.session.query(Customer).get(customer_id)
        if customer is None:
            abort(404)
        return jsonify(customer.to_dict()), 200


@views_bp.route('/users/<user_id>/customers',
                methods=['GET'], strict_slashes=False)
def get_user_customers(user_id):
    """
    Get all customers for a user
    """
    with app.app_context():
        customers = db.session.query(Customer).filter_by(user_id=user_id)\
            .order_by(desc(Customer.created_at)).all()
        data = [customer.to_dict() for customer in customers]
        return jsonify(data), 200


@views_bp.route('/users/<user_id>/customers',
                methods=['POST'], strict_slashes=False)
def post_customer(user_id):
    """
    Add a customer
    """
    with app.app_context():
        if request.is_json:
            data = request.get_json()
            not_needed = ['id', 'created_at', 'updated_at']
            for value in not_needed:
                if value in data:
                    abort(400,
                          'id, created_at and updated_at are not needed')
            required = ['code', 'name']
            for value in required:
                if value not in data:
                    abort(400, f'{value} is required')
            data['user_id'] = user_id
            id = uuid4()
            customer = Customer(id=id, **data)
            db.session.add(customer)
            db.session.commit()
            return jsonify({"message": "customer added successfully"}), 200
        else:
            abort(400, 'Not a JSON')


@views_bp.route('/customers/<customer_id>',
                methods=['DELETE'], strict_slashes=False)
def delete_customer(customer_id):
    """
    Delete a customer
    """
    with app.app_context():
        customer = db.session.query(Customer).get(customer_id)
        if customer is None:
            abort(404)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "customer deleted successfully"}), 200


@views_bp.route('/customers/<customer_id>',
                methods=['PUT'], strict_slashes=False)
def update_customer(customer_id):
    """
    Update a customer
    """
    with app.app_context():
        customer = db.session.query(Customer).get(customer_id)
        if customer is None:
            abort(404)
        if request.is_json:
            data = request.get_json()
            not_required = ['id', 'created_at', 'updated_at', 'user_id']
            for key, value in data.items():
                if key in not_required:
                    continue
                else:
                    setattr(customer, key, value)
            Customer.save(customer)
            db.session.commit()
            return jsonify({"message": "customer updated successfully"}), 200
        else:
            abort(400, 'Not a JSON')
