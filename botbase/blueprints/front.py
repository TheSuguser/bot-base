from flask import Blueprint
from flask import url_for, redirect, render_template
from flask_login import login_required

front_bp = Blueprint('front', __name__)

@front_bp.route('/')
def index():
    return render_template('front/index.html')

@front_bp.route('/panel')
@login_required
def panel():
    return render_template('front/panel.html')