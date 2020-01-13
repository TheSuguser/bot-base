from flask import render_template, redirect, flash, url_for

def init_app(app):
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html', title="INDEX")
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        from .forms import LoginForm
        form = LoginForm()
        # 验证数据
        if form.validate_on_submit():
            flash('用户登录的名户名是:{} , 是否记住我:{}'.format(
                form.username.data,
                form.remember_me.data))
            return redirect('/index')
        return render_template('login.html', title='Login', form=form)

        
    @app.route('/success')
    def success():
        print("ssss")
        return "success"

