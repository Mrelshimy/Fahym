from flask import jsonify, abort, request
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import Investment, User
from uuid import uuid4


@views_bp.route('/investments', methods=['GET'], strict_slashes=False)
def get_investments():
    """
    Get all investments
    """
    with app.app_context():
        items = db.session.query(Investment).\
            order_by(Investment.created_at).all()
        data = [item.to_dict() for item in items]
        return jsonify(data), 200


@views_bp.route('/users/<user_id>/initial_investment',
                methods=['GET'], strict_slashes=False)
def get_initial_investment(user_id):
    """
    Get the initial investment for a user
    """
    with app.app_context():
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            items = db.session.query(Investment).filter_by(user_id=user_id)\
                .order_by(Investment.created_at).all()
            data = [item.to_dict() for item in items]
            return jsonify(data[-1]), 200
        else:
            abort(404, 'User not found')


@views_bp.route('users/<user_id>/investments',
                methods=['GET'], strict_slashes=False)
def get_user_investments(user_id):
    """
    Get all investments for a user
    """
    with app.app_context():
        items = db.session.query(Investment).filter_by(user_id=user_id)\
            .order_by(Investment.created_at).all()
        data = [item.to_dict() for item in items]
        return jsonify(data), 200


@views_bp.route('users/<user_id>/investments',
                methods=['POST'], strict_slashes=False)
def add_investments(user_id):
    """
    Add an investment
    """
    with app.app_context():
        if request.is_json:
            user = db.session.query(User).filter_by(id=user_id).first()
            if (user):
                data = request.get_json()
                not_required = ['id', 'created_at', 'updated_at']
                for value in not_required:
                    if value in data:
                        abort(400, f'{value} is not required')
                required = ['name', 'date', 'amount']
                for value in required:
                    if value not in data:
                        abort(400, f'{value} is required')
                data['user_id'] = user_id
                data['id'] = str(uuid4())
                investment = Investment(**data)
                db.session.add(investment)
                db.session.commit()
                return jsonify({"message": "Investment added"}), 200
            else:
                abort(404, 'User not found')
        else:
            abort(400, 'Request is not JSON')
