from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_login import LoginManager, AnonymousUserMixin

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()

class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False
    def can(self, permission_name):
        return False

login_manager.anonymous_user = Guest

@login_manager.user_loader
def load_user(user_id):
    from botbase.models import User
    user = User.query.get(int(user_id))
    return user