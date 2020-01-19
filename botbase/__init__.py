import os

import click

from flask import Flask
from flask import redirect, url_for

from botbase.blueprints.auth import auth_bp
from botbase.blueprints.front import front_bp
from botbase.blueprints.admin import admin_bp
from botbase.extensions import db, bootstrap, login_manager


def create_app(config=None):
    app = Flask(__name__)

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

    
    register_extension(app)
    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(front_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 临时代码 从主页跳转到login
    # @app.route('/')
    # def index():
    #     return redirect(url_for('auth.login'))

def register_extension(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)


# 创建管理员帐号
def register_commands(app):
    @app.cli.command()
