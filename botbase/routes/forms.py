from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    #DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('Username', validators=[DataRequired(message="Please input username")])
    password = PasswordField('Password', validators=[DataRequired(message="Please input password")])
    remember_me = BooleanField('rememberMe')
    submit = SubmitField('LOGIN IN')