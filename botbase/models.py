from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from botbase.extensions import db


# 角色与权限模型
# relationship table
roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id',db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'User': ['DESIGN'],
            'Administrator': ['DESIGN', 'ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()

    def __repr__(self):
        return "<Role: {}>".format(self.name)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # 定义关系
    bots = db.relationship('BotObject')

    # 定义权限
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_role(self):
        if self.role is None:
            if self.email in current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()
    
    @property
    def is_admin(self):
        return self.role.name == "Administrator"
    
    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions
    
    def __repr__(self):
        return '<username:{}>'.format(self.username)    
class BotObject(db.Model):
    __tablename__ = 'botobject'
    id = db.Column(db.Integer, primary_key=True)
    chatbot_id = db.Column(db.String(120), unique=True)
    # 定义外键
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

class QASet(db.Model):
    __tablename__ = 'qaset'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128), unique=True)
    db.Column(db.Text)
    topic = db.Column(db.String(50))

    #定义外键
    chatbot_id = db.Column(db.Integer, db.ForeignKey('botobject.id'))


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    area = db.Column(db.String(200), default='')
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))