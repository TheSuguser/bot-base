from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user

from botbase.models import User, Project
from botbase.forms import ProjectForm
from botbase.extensions import db
from botbase.utils import redirect_back
from botbase.decorators import only_owner_can

front_bp = Blueprint('front', __name__)

@front_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('front.panel'))
    return render_template('front/index.html')

@front_bp.route('/panel')
@login_required
def panel():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('front/panel.html', projects=projects)

@front_bp.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        name = form.name.data
        area = form.area.data 
        user_id = current_user.id
        project = Project(name=name, area=area, user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('front.panel'))
    return render_template('front/create_project.html', form=form)

@front_bp.route('/project/<int:project_id>/delete', methods=['POST'])
@only_owner_can
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'success')
    return redirect_back()