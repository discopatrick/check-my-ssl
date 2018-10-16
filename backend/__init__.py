import os

from flask import (
    abort,
    Flask,
    jsonify,
    request,
)
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    @app.route('/check-ssl', methods=['POST'])
    def check_ssl():
        url = request.get_json().get('url')

        if not url:
            abort(400)

        app.logger.info(f'Checking SSL for url: {url}')

        return jsonify(
            days_until_ssl_expiry=10,
            action_needed=True,
        )

    return app
