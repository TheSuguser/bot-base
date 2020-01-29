from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user

from botbase.models import User, Project, Bot, QASet
from botbase.forms import ProjectForm, BotForm, QAForm
from botbase.extensions import db
from botbase.utils import redirect_back
from botbase.decorators import admin_required, only_owner_can

bot_bp = Blueprint('bot', __name__)

@bot_bp.route("/<int:project_id>/<int:bot_id>", methods=['GET','POST'])
@only_owner_can
@login_required
def index(project_id, bot_id):
    return render_template('bot/index.html',project_id=project_id, bot_id=bot_id)

# TODO 添加轮询
@bot_bp.route("<int:project_id>/<int:bot_id>/qa", methods=['GET','POST'])
@only_owner_can
@login_required
def qa(project_id, bot_id):
    qa_set = QASet.query.filter_by(bot_id=bot_id).all()
    return render_template('bot/qa.html', project_id=project_id, bot_id=bot_id, qa_set=qa_set)

@bot_bp.route('<int:project_id>/<int:bot_id>/add_qa', methods=['GET', 'POST'])
@only_owner_can
@login_required
def add_qa(project_id, bot_id):
    form=QAForm()
    if form.validate_on_submit():
        q = form.question.data 
        a = form.answer.data 
        t = form.topic.data 
        qa = QASet(
            question=q,
            answer=a,
            topic=t,
            bot_id=bot_id
        )
        db.session.add(qa)
        db.session.commit()
        flash("新的问题添加成功", "info")
        return redirect(url_for('bot.qa', project_id=project_id, bot_id=bot_id))
    return render_template('bot/add_qa.html', form=form, project_id=project_id, bot_id=bot_id)


@bot_bp.route('<int:project_id>/<int:bot_id>/<int:qa_id>/delete_qa', methods=['POST'])
@only_owner_can
@login_required
def delete_qa(project_id, bot_id, qa_id):
    qa = QASet.query.get_or_404(qa_id)
    db.session.delete(qa)
    db.session.commit()
    flash('该问答对已删除', 'success')
    return redirect_back()