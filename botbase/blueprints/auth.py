from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from botbase.forms import LoginForm, TrialForm
from botbase.models import Admin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('front.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data 
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back')
                return redirect(url_for('admin.setting'))
            flash('无效的用户名和密码')
        else:
            flash('No account')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logout success.')
    return redirect(url_for('front.index'))

@auth_bp.route('/trial', methods=['GET', 'POST'])
def trial():
    form = TrialForm()
    if form.validate_on_submit():
        flash("您的申请已发送，请等待回复")
        return redirect(url_for('front.index'))
    return render_template('auth/trial.html', form=form)