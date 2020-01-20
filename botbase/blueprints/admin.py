from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from botbase.forms import RegisterForm
from botbase.models import User
from botbase.extensions import db
from botbase.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

# @admin_bp.route('/index')
# def setting():
#     return render_template('admin/index.html')

@admin_bp.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data 
        password = form.password.data 

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash("新用户 {} 添加成功".format(username))
        
        return redirect(url_for('front.panel'))

    return render_template('admin/register.html', form=form)


    