from flask import Blueprint
from flask import render_template, flash, redirect, url_for

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'hello'

@auth_bp.route('logout')
def logout():
    pass