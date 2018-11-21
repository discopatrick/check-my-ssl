from logging.config import dictConfig
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[FlaskIntegration()],
)

ENV = os.environ['ENV']
LOGZIO_FORMAT = '{"env": "' + ENV + '"}'

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'logzioFormat': {
            'format': LOGZIO_FORMAT,
        },
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default',
        },
        'logzio': {
            'class': 'logzio.handler.LogzioHandler',
            'level': 'INFO',
            'formatter': 'logzioFormat',
            'token': os.environ['LOGZIO_TOKEN'],
            'logzio_type': "python",
            'logs_drain_timeout': 5,
            'url': 'https://listener.logz.io:8071',
            'debug': True,
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'logzio'],
    },
})
