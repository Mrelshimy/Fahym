from flask import jsonify, abort, request
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import User


@views_bp.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Get all users
    """
    with app.app_context():
        users = db.session.query(User).all()
        data = [user.to_dict() for user in users]
        return jsonify(data), 200


@views_bp.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Get a single user
    """
    with app.app_context():
        user = db.session.query(User).get(user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict()), 200


@views_bp.route('users/', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Add a user
    """
    with app.app_context():
        if request.is_json:
            data = request.get_json()
            if 'id' in data or\
                'created_at' in data or\
                    'updated_at' in data:
                abort(400, 'id, created_at and updated_at are not needed')
            if 'buss_name' not in data:
                abort(400, 'Bussiness name is missing')
            if 'email' not in data:
                abort(400, 'email is missing')
            if 'password' not in data:
                abort(400, 'Password is missing')
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "User added successfully"}), 200
        else:
            abort(400, 'Not a JSON')


@views_bp.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Delete a user
    """
    with app.app_context():
        user = db.session.query(User).get(user_id)
        if user is None:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200


@views_bp.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update a user
    """
    with app.app_context():
        user = db.session.query(User).get(user_id)
        if user is None:
            abort(404)
        if request.is_json:
            data = request.get_json()
            not_required = ['id', 'created_at',
                            'updated_at', 'email', 'password']
            for key, value in data.items():
                if key in not_required:
                    continue
                else:
                    setattr(user, key, value)
            User.save(user)
            db.session.commit()
            return jsonify({"message": "User updated successfully"}), 200
        else:
            abort(400, 'Not a JSON')
