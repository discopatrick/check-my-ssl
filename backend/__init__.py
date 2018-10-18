import os

from flask import (
    abort,
    escape,
    Flask,
    jsonify,
    request,
)
from flask_cors import CORS

from backend.database import db_session
from backend.models import DomainName
from ssl_checker.ssl_checker import days_until_ssl_expiry


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

    @app.route('/domain-names')
    def domain_names():
        all_domain_names = db_session.query(DomainName).all()
        return escape(str(all_domain_names))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
