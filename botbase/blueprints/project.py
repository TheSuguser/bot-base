from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user

from botbase.models import User, Project, Bot
from botbase.forms import ProjectForm, BotForm
from botbase.extensions import db
from botbase.utils import redirect_back
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
