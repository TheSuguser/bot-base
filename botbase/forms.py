from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    #DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名', validators=[DataRequired(message="Please input username")])
    password = PasswordField('密码', validators=[DataRequired(message="Please input password"), Length(8,16)])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')