import os

from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory, send_file
from flask_login import login_required, current_user

from botbase.models import User, Project, Bot
from botbase.forms import ProjectForm, BotForm, ProjectConfigForm
from botbase.extensions import db
from botbase.utils.flask_tool import redirect_back
from botbase.utils.create_bot import create_qa_bot
from botbase.decorators import admin_required, only_owner_can

project_bp = front_bp = Blueprint('project', __name__)

@project_bp.route('/<int:project_id>/index')
@only_owner_can
@login_required
def index(project_id):
    bots = Bot.query.filter_by(user_id=current_user.id).all()
    return render_template('project/index.html', project_id=project_id, bots=bots)

@project_bp.route('<int:project_id>/create_bot', methods=['GET', 'POST'])
@only_owner_can
@login_required
def create_bot(project_id):
    form = BotForm()
    if form.validate_on_submit():
        name = form.name.data 
        bot_type = form.bot_type.data
        lang = form.lang.data
        bot = Bot(
            name=name,
            bot_type=bot_type,
            lang=lang,
            project_id=project_id,
            user_id=current_user.id
        )
        db.session.add(bot)
        db.session.commit()
        if bot_type == 1:
            create_qa_bot(bot.id)
        flash('ChatBot添加完毕', 'info')
        return redirect(url_for('project.index', project_id=project_id))
    return render_template('project/create_bot.html', form=form, project_id=project_id)

@project_bp.route('/<int:project_id>/<int:bot_id>/delete', methods=['POST'])
@only_owner_can
@login_required
def delete_bot(project_id, bot_id):
    bot = Bot.query.get_or_404(bot_id)
    db.session.delete(bot)
    db.session.commit()
    flash('Bot deleted.', 'success')
    return redirect_back()

@project_bp.route('<int:project_id>/project_config', methods=['GET', 'POST'])
@only_owner_can
@login_required
def config(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectConfigForm(
        name = project.name,
        welcome=project.welcome,
        unknown=project.unknown
    )

    if form.validate_on_submit():
        project.name = form.name.data
        project.welcome = form.welcome.data 
        project.unknown = form.unknown.data 
        
        if form.bot_avatar.data:
            bot_avatar = form.bot_avatar.data
            ext = os.path.splitext(bot_avatar.filename)[1]
            filename = os.path.join(current_app.config['AVATAR_PATH'], "bot_{}{}".format(project_id, ext))
            bot_avatar.save(filename)
            project.bot_avatar = filename
        
        if form.user_avatar.data:
            user_avatar = form.user_avatar.data
            ext = os.path.splitext(user_avatar.filename)[1]
            filename = os.path.join(current_app.config['AVATAR_PATH'], "user_{}{}".format(project_id, ext))
            user_avatar.save(filename)
            project.user_avatar = filename

        db.session.commit()
        flash('项目设置修改成功', 'success')
        render_template('project/config.html', project_id=project_id, form=form)
    return render_template('project/config.html', project_id=project_id, form=form)
    
@project_bp.route('<int:project_id>/get_bot_avatar', methods=['GET'])
def get_bot_avatar(project_id):
    project = Project.query.get_or_404(project_id)
    return send_file(os.path.join(current_app.config['AVATAR_PATH'], project.bot_avatar))

@project_bp.route('<int:project_id>/get_user_avatar', methods=['GET'])
def get_user_avatar(project_id):
    project = Project.query.get_or_404(project_id)
    return send_file(os.path.join(current_app.config['AVATAR_PATH'], project.user_avatar))