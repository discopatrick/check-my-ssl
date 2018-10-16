import os

from flask import (
    Flask,
    jsonify,
)
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    @app.route('/check-ssl')
    def check_ssl():
        return jsonify(
            days_until_ssl_expiry=10,
            action_needed=True,
        )

    return app
