from flask import Blueprint
from flask import render_template

from botbase.forms import RegisterForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/setting')
def setting():
    return render_template('admin/setting.html')

@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        pass 
    
    return render_template('admin/register.html', form=form)


    