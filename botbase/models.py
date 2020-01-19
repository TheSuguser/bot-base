from botbase.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # 定义关系
    bots = db.relationship('BotObject')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(password)
    
    
    def __repr__(self):
        return '<username:{}>'.format(self.username)

class Admin(db.Model, UserMixin):

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
    answer = db.Column(db.text())
    topic = db.Column(db.String(50))

    #定义外键
    chatbot_id = db.Column(db.Integer, db.ForeignKey('botobject.id'))
    