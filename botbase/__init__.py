import os

from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    # load default configuration
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
    
    from botbase import routes
    routes.init_app(app)
    from botbase import models
    models.init_app(app)
    return app

