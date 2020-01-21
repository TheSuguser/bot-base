from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user

from botbase.models import User, Project
from botbase.forms import ProjectForm
from botbase.extensions import db
from botbase.utils import redirect_back
from botbase.decorators import admin_required, only_onwer_can

project_bp = front_bp = Blueprint('project', __name__)

@project_bp.route('/<int:project_id>/index')
@only_onwer_can
def index(project_id):
    return render_template('project/index.html')
