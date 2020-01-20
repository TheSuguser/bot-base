from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    #DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名', validators=[DataRequired(message="Please input username")])
    password = PasswordField('密码', validators=[DataRequired(message="Please input password")])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')

class TrialForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message="Please input email"), Email(message="请输入合法的邮箱地址")])
    department = StringField('部门')
    reason = StringField('业务场景')
    submit = SubmitField('申请')

class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message="Please input email"), Email(message="请输入合法的邮箱地址")])
    username = StringField('用户名', validators=[DataRequired(message="Please input username")])
    password = PasswordField('密码', validators=[DataRequired(message="Please input password")])
    password_conf = PasswordField('请再次确认密码', validators=[DataRequired(message="Please input password"), EqualTo("password")])
    submit = SubmitField('注册')