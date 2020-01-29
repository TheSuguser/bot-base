import os
BASE_DIR = os.path.abspath('')

# 调试信息
DEBUG = True
PORT = 5003

# Secure key
SECRET_KEY = 'botbasetest'

# mysql设置
#格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:dai@localhost:3307/flasktest?charset=utf8'
#如果你不打算使用mysql，使用这个连接sqlite也可以
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 上传设置
MAXN_CONTENT_LENGTH = 10 * 1024 * 1024

ADMIN_EMAIL = ["joezheng@deloitte.com.cn"]

# 问答集上传设置
QA_PER_PAGE = 10

