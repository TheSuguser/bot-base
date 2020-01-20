from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from botbase.forms import LoginForm, TrialForm
from botbase.models import User

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
        user = User.query.filter_by(username=username.lower()).first()

        if user is not None and user.validate_password(password):
            login_user(user, remember)
            flash('welcome back', 'info')
            return redirect(url_for('front.index'))
        else:
            flash('无效的账户或密码', 'warning')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)
    

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('front.index'))

@auth_bp.route('/trial', methods=['GET', 'POST'])
def trial():
    form = TrialForm()
    if form.validate_on_submit():
        flash("您的申请已发送，请等待回复")
        return redirect(url_for('front.index'))
    return render_template('auth/trial.html', form=form)