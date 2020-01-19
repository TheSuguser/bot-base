from flask import Blueprint
from flask import url_for, redirect, render_template

front_bp = Blueprint('front', __name__)

@front_bp.route('/')
def index():
    return render_template('front/index.html')