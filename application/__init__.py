from flask import Flask, request, redirect
from flask_cors import CORS
from config import configure_app
from flask_session import Session
import traceback

application = Flask(__name__)

cors = CORS(application, origins=['http://localhost:5173'])
application.config['CORS_HEADERS'] = 'Content-Type'

configure_app(application)
Session(application)

@application.errorhandler(500)
def internal_server_error(error):
    print(traceback.format_exc())
    application.logger.error('Client Error: {}, path: {}'.format(error, request.path))

    if ('localhost:5000' in request.host_url):
        error = 'Server Error: %s', (error)
        return error
    else:
        return redirect('/something-went-wrong')

@application.errorhandler(404)
def page_not_found(error):
    print(traceback.format_exc())
    application.logger.error('Client Error: {}, path: {}'.format(error, request.path))

    if ('localhost:5000' in request.host_url):
        error = 'Client Error %s', (error)
        return error
    else:
        return redirect('/something-went-wrong')

@application.errorhandler(Exception)
def unhandled_exception(error):
    print(traceback.format_exc())
    application.logger.error('Client Error: {}, path: {}'.format(error, request.path))
    
    if ('localhost:5000' in request.host_url or 'localhost:5173' in request.host_url):
        error = 'Unhandled Exception %s', (error)
        return error
    else:
        return redirect('/something-went-wrong')

from application.views import main
application.register_blueprint(main.mod)

if __name__ == 'application':
    from application import views