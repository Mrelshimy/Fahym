from flask import Flask, jsonify, make_response
from acc_app.api.v1.views import views_bp
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/acc_app/api/*": {"origins": '*'}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(views_bp)


@app.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
