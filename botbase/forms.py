from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired

from botbase.models import User, QASet

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

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("The username is already used")
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("The email is already used")



class ProjectForm(FlaskForm):
    name = StringField('项目名称', validators=[DataRequired(message="Please input name")])
    area = StringField('应用场景(Optional)', default='')
    submit = SubmitField('创建项目')

class BotForm(FlaskForm):
    name = StringField('ChatBot名称', validators=[DataRequired(message="Please input name")])
    lang = SelectField(
        label='语言', 
        validators=[DataRequired('Please select language')], 
        choices=[(1,"中文"), (2, "English")], 
        default=1,
        coerce = int)
    bot_type = SelectField(
        label='机器人类别', 
        validators=[DataRequired('Please select bot type')],
        choices=[(1,"问答型"), (2, "闲聊型")], 
        default=1,
        coerce = int)
    submit = SubmitField('创建机器人')

class QAForm(FlaskForm):
    question = StringField('问题', validators=[DataRequired(message="请输入问题")])
    answer = StringField('答案', validators=[DataRequired(message="请输入答案")])
    topic = StringField('类别', validators=[DataRequired(message="请输入类别")])
    submit = SubmitField('添加')

class UploadQAForm(FlaskForm):
    qa_set = FileField("上传文件（仅支持xlsx格式）", validators=[FileRequired(), FileAllowed(['xlsx'])])
    cover = BooleanField('清空原有数据')
    submit = SubmitField('上传')

class SynWordForm(FlaskForm):
    base_word = StringField('原词', validators=[DataRequired(message="请输入原词")])
    synword = StringField('答案', validators=[DataRequired(message="请输入同义词")])
    submit = SubmitField('添加')

class StopWordForm(FlaskForm):
    word = StringField('停用词', validators=[DataRequired(message="请输入原词")])
    submit = SubmitField('添加')


class QABotBasicForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(message="请输入机器人姓名")])
    welcome = StringField('欢迎语', validators=[DataRequired(message="请输入机器人欢迎语")])
    unknown = StringField('澄清语', validators=[DataRequired(message="请输入澄清玉")])
    k1 = SelectField(
        '多选问题选项数量',
        choices=[(0,0), (1,1), (2,2), (3,3), (4,4), (5,5)],
        default=5,
        validators=[DataRequired()])

class ProjectConfigForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(message="请输入机器人姓名")])
    welcome = StringField('欢迎语', validators=[DataRequired(message="请输入机器人欢迎语")])
    unknown = StringField('澄清语', validators=[DataRequired(message="请输入澄清语")])
    submit = SubmitField('保存')
