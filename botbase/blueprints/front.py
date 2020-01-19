from flask import Blueprint
from flask import url_for, redirect

front_bp = Blueprint('front', __name__)

@front_bp.route('/')
def index():
    return redirect(url_for('auth.login'))