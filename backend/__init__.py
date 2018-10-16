import os

from flask import (
    abort,
    Flask,
    jsonify,
    request,
)
from flask_cors import CORS

from ssl_checker.check_my_ssl import days_until_ssl_expiry


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

        days_left = days_until_ssl_expiry(url)
        take_action = days_left <= 28

        return jsonify(
            days_until_ssl_expiry=days_left,
            action_needed=take_action,
        )

    return app
