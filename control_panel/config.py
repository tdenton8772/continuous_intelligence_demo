import logging
import os
from logging.handlers import RotatingFileHandler

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_to_a_secure_value")
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/messaging.log")
    LOGGING_LEVEL = logging.DEBUG
    AWS_PROFILE = os.environ.get("AWS_PROFILE", "default")
    SESSION_PERMANENT = True
    SESSION_TYPE = os.environ.get("SESSION_TYPE", "filesystem")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    TEMPLATES_AUTO_RELOAD = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG

class ProductionConfig(BaseConfig):
    DEBUG = False
    LOGGING_LEVEL = logging.WARNING
    WTF_CSRF_ENABLED = True

config = {
    "development": "config.DevelopmentConfig",
    "production": "config.ProductionConfig",
    "default": "config.BaseConfig"
}

def configure_app(application):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    application.config.from_object(config[config_name])

    # Configure logging
    if not os.path.exists(os.path.dirname(application.config['LOGGING_LOCATION'])):
        os.makedirs(os.path.dirname(application.config['LOGGING_LOCATION']))

    handler = RotatingFileHandler(application.config['LOGGING_LOCATION'], maxBytes=10485760, backupCount=5)
    handler.setLevel(application.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(application.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    
    application.logger.addHandler(handler)
    application.logger.setLevel(application.config['LOGGING_LEVEL'])
