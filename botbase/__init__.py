import os

import click

from flask import Flask
from flask import redirect, url_for

from botbase.blueprints.auth import auth_bp
from botbase.blueprints.front import front_bp
from botbase.blueprints.admin import admin_bp
from botbase.extensions import db, bootstrap, login_manager
from botbase.models import Admin


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
    register_commands(app)

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
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username
            )
            admin.set_password(password)
            db.session.add(admin)

        # category = Category.query.first()
        # if category is None:
        #     click.echo('Creating the default category...')
        #     category = Category(name='Default')
        #     db.session.add(category)

        db.session.commit()
        click.echo('Done.')
