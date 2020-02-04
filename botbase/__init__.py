import os

import click
import logging

from flask import Flask
from flask import redirect, url_for, render_template
from logging.handlers import RotatingFileHandler

from botbase.blueprints.auth import auth_bp
from botbase.blueprints.front import front_bp
from botbase.blueprints.admin import admin_bp
from botbase.blueprints.project import project_bp
from botbase.blueprints.bot import bot_bp
from botbase.extensions import db, bootstrap, login_manager, csrf
from botbase.models import User, Role


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
    register_errorhandlers(app)
    register_commands(app)
    register_logging(app)

    return app


def register_blueprints(app):
    app.register_blueprint(front_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(project_bp, url_prefix='/project')
    app.register_blueprint(bot_bp, url_prefix='/bot')

    # 临时代码 从主页跳转到login
    # @app.route('/')
    # def index():
    #     return redirect(url_for('auth.login'))

def register_extension(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

def register_errorhandlers(app):
    # 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

def register_logging(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(messges)s')

    file_handler = RotatingFileHandler(
        app.config['LOG_PATH'],
        maxBytes=app.config['LOG_MAX_BYTES'],
        backupCount=app.config['LOG_BACKUP_COUNT']
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


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
    @click.option('--email', prompt=True)
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(email, username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        # admin = Admin.query.first()

        # if admin is not None:
        #     click.echo('The administrator already exists, updating...')
        #     admin.username = username
        #     admin.set_password(password)
        # else:
        #     click.echo('Creating the temporary administrator account...')
        #     admin = Admin(
        #         username=username
        #     )
        #     admin.set_password(password)
        #     db.session.add(admin)
        # db.session.commit()
        # click.echo('Done.')

        """initial roles and permissions"""
        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Done.')

        """initial a account"""
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        click.echo("创建的是 <{}> 账户".format(user.role.name))
        db.session.add(user)
        db.session.commit()
        click.echo("账户 <{}> 创建完成".format(user.username))

        # category = Category.query.first()
        # if category is None:
        #     click.echo('Creating the default category...')
        #     category = Category(name='Default')
        #     db.session.add(category)

        
