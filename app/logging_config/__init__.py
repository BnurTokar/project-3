import logging
from logging.config import dictConfig

import flask
from flask import request, current_app

from app.logging_config.log_formatters import RequestFormatter

log_con = flask.Blueprint('log_con', __name__)


@log_con.before_app_request
def before_request_logging():
    current_app.logger.info("Before Request")
    debug_log = logging.getLogger("myDebug")
    request_log = logging.getLogger("myRequest")

    debug_log.debug("mydebugs logging in before_request_logging")
    request_log.info("request before logging")

@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response
    current_app.logger.info("After Request")

    debug_log = logging.getLogger("myDebug")
    request_log = logging.getLogger("myRequest")

    debug_log.debug("mydebugs logging in after_request_logging")
    request_log.info("request after logging")

    return response


@log_con.before_app_first_request
def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

    debug_log = logging.getLogger("myDebug")
    request_log = logging.getLogger("myRequest")

    debug_log.debug("mydebugs logging in configure_logging")
    request_log.info("configure logging request")


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s from [%(levelname)s] %(name)s: %(message)s'
        },
        'RequestFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '[%(asctime)s] [%(levelname)s] [%(process)d] %(remote_addr)s requested %(url)s \n'
                        '%(levelname)s in %(module)s: %(message)s'
        },
        'DebugFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '[%(asctime)s] [%(levelname)s] IP: %(ip)s requested %(url)s \n'
                        'Module: %(module)s  Message: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app/logs/flask.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.mydebug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'DebugFormatter',
            'filename': 'app/logs/debug.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myrequest': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'RequestFormatter',
            'filename': 'app/logs/request.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default','file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {
            'handlers': ['default','file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'myDebug': {
            'handlers': ['file.handler.mydebug'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myRequest': {
            'handlers': ['file.handler.myrequest'],
            'level': 'INFO',
            'propagate': False
        },
    }
}