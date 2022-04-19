import flask

error_handlers = flask.Blueprint('error_handlers', __name__)

@error_handlers.app_errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404