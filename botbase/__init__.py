import os

from flask import Flask

from botbase.extensions import db


def create_app(config=None):
    app = Flask(__name__)

    register_logging(app)
    register_extension(app)


def register_logging(app):
    app.config.from_object('botbase.settings')
    # load environment configuration
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')
    
    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

def register_blueprints(app):
    pass

def register_extension(app):
    db.init_app(app)
