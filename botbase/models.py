from botbase.extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    # 定义关系
    bots = db.relationship('BotObject')
    
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
    answer = db.Column(db.text())
    topic = db.Column(db.String(50))

    #定义外键
    chatbot_id = db.Column(db.Integer, db.ForeignKey('botobject.id'))
    