from flask import jsonify, abort, request
from acc_app.api.v1.views import views_bp
from acc_app import db, app
from acc_app.models.models import User, sales_item


@views_bp.route('/users/<user_id>/sales_items',
                methods=['GET'], strict_slashes=False)
def get_sales_items(user_id):
    """
    Get all sales items for a user
    """
    with app.app_context():
        user = db.session.query(User).get(user_id)
        if user is None:
            abort(404)
        items = sales_item.query.all()
        items_list = [
            {
                'id': item.id,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'item_id': item.item_id,
                'sales_invoice_id': item.purchase_invoice_id,
                'item_quantity': item.item_quantity,
                'item_price': item.item_price
            }
            for item in items
        ]
        return jsonify(items_list), 200
