from flask import (
    abort,
    Flask,
    jsonify,
    request,
)
from flask_cors import CORS

from web.database import db_session
import web.logging_config
from web.models import DomainName
from ssl_checker import days_until_ssl_expiry


def init_db():
    import web.models
    from web.models import Base
    from web.database import engine
    Base.metadata.create_all(bind=engine)


def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db()

    @app.route('/hello')
    def hello():
        app.logger.info('/hello')
        return 'Hello World!'

    @app.route('/check-ssl', methods=['POST'])
    def check_ssl():
        app.logger.info('/check-ssl')

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
        app.logger.info('/domain-names')
        all_domain_names = db_session.query(DomainName).all()
        return jsonify(domain_names=[dn.domain_name for dn in all_domain_names])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
