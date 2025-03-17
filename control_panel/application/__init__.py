import traceback
import logging
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
from config import configure_app
from flask_session import Session

# Initialize Flask application
application = Flask(__name__)

# Enable CORS
cors = CORS(application, origins=['http://localhost:5173'])
application.config['CORS_HEADERS'] = 'Content-Type'

# Configure application settings
configure_app(application)
Session(application)

# Configure error logging
logger = application.logger
logger.setLevel(application.config["LOGGING_LEVEL"])

# Enhanced error handlers
def log_exception(error, status_code):
    error_traceback = traceback.format_exc()
    request_info = f"Method: {request.method}, Path: {request.path}, Data: {request.get_json(silent=True)}"

    logger.error(f"Error {status_code}: {error}\nTraceback:\n{error_traceback}\nRequest Info: {request_info}")

    return jsonify({"error": str(error), "status": status_code}), status_code

@application.errorhandler(500)
def internal_server_error(error):
    return log_exception(error, 500)

@application.errorhandler(404)
def page_not_found(error):
    return log_exception(error, 404)

@application.errorhandler(Exception)
def unhandled_exception(error):
    return log_exception(error, 500)

# Import and register Blueprints
from application.views import main
application.register_blueprint(main.mod)

from application.views import api
application.register_blueprint(api.mod)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)
