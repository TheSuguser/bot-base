from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from botbase.forms import LoginForm

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
        

    return render_template('auth/login.html')

@auth_bp.route('logout')
def logout():
    pass