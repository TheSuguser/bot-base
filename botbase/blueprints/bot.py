from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory, request
from flask_login import login_required, current_user

from botbase.models import User, Project, Bot, QASet, SynWord, StopWord, QABot
from botbase.forms import ProjectForm, BotForm, QAForm, UploadQAForm, SynWordForm, StopWordForm, QABotBasicForm
from botbase.extensions import db
from botbase.utils.flask_tool import redirect_back
from botbase.decorators import admin_required, only_owner_can

from xlrd import open_workbook

import re

bot_bp = Blueprint('bot', __name__)

# @bot_bp.route("/<int:project_id>/<int:bot_id>", methods=['GET','POST'])
# @only_owner_can
# @login_required
# def index(project_id, bot_id):
#     return render_template('bot/index.html',project_id=project_id, bot_id=bot_id)

@bot_bp.route("/<int:project_id>/<int:bot_id>", methods=['GET','POST'])
@bot_bp.route("<int:project_id>/<int:bot_id>/qa", methods=['GET','POST'])
@only_owner_can
@login_required
def qa(project_id, bot_id):
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['QA_PER_PAGE']
    pagination = QASet.query.filter_by(bot_id=bot_id).paginate(page, per_page=per_page)
    qa_set = pagination.items
    return render_template('bot/qa.html', project_id=project_id, bot_id=bot_id, pagination=pagination, qa_set=qa_set)

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
        flash("新的问题添加成功", "success")
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

# TODO 改为模态框实现 可能需要js协助
@bot_bp.route('<int:project_id>/<int:bot_id>/<int:qa_id>/edit_qa', methods=['GET', 'POST'])
@only_owner_can
@login_required
def edit_qa(project_id, bot_id, qa_id):
    qa_set = QASet.query.get(qa_id)

    form = QAForm(
        question=qa_set.question,
        answer=qa_set.answer,
        topic=qa_set.topic)
    form.submit.label.text = "保存"

    if form.validate_on_submit():
        qa_set.answer=form.answer.data
        qa_set.question=form.question.data 
        qa_set.topic=form.topic.data 
        db.session.commit()
        flash('问题修改成功', 'success')
        return redirect(url_for('bot.qa', project_id=project_id, bot_id=bot_id))
    return render_template('bot/edit_qa.html', project_id=project_id, bot_id=bot_id, qa_id=qa_id, form=form)

@bot_bp.route('<int:project_id>/<int:bot_id>/upload_qa', methods=['GET', 'POST'])
@only_owner_can
@login_required
def upload_qa(project_id, bot_id):
    form = UploadQAForm()

    if form.validate_on_submit():
        qa_set = form.qa_set.data
        cover = form.cover.data 
        update_cnt = 0
        add_cnt = 0
        workbook = open_workbook(file_contents=qa_set.read())
        
        if cover:
            qas = QASet.query.filter_by(bot_id=bot_id).all()
            for _ele in qas:
                db.session.delete(_ele)
        try:
            for table in workbook.sheets():
                qs = table.col_values(0)
                ans = table.col_values(1)
                ts = table.col_values(2)
                for i in range(1, min([len(qs), len(ans), len(ts)])):
                    _qa = QASet.query.filter_by(bot_id=bot_id).filter_by(question=qs[i]).first()
                    if _qa:
                        _qa.answer=ans[i]
                        _qa.topic=ts[i]
                        db.session.commit()
                        update_cnt+=1
                    else:
                        _qa = QASet(
                            question=qs[i],
                            answer=ans[i],
                            topic=ts[i],
                            bot_id=bot_id
                        )
                        db.session.add(_qa)
                        add_cnt += 1
            db.session.commit()
            flash('成功上传{}个问答对, 增加了{}条，更新了{}条'.format(add_cnt+update_cnt, add_cnt, update_cnt), 'success')
            return redirect(url_for('bot.qa', project_id=project_id, bot_id=bot_id)) 
        except Exception as e:
            flash('上传错误，报错为: {}'.format(e), 'danger')
            return render_template('bot/upload_qa.html',form=form, project_id=project_id, bot_id=bot_id)
           
    return render_template('bot/upload_qa.html',form=form, project_id=project_id, bot_id=bot_id)
    

@bot_bp.route("<int:project_id>/<int:bot_id>/synword", methods=['GET','POST'])
@only_owner_can
@login_required
def synword(project_id, bot_id):
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['QA_PER_PAGE']
    pagination = SynWord.query.filter_by(bot_id=bot_id).paginate(page, per_page=per_page)
    synwords = pagination.items
    return render_template('bot/synword.html', project_id=project_id, bot_id=bot_id, pagination=pagination, synwords=synwords)

@bot_bp.route('<int:project_id>/<int:bot_id>/add_synword', methods=['GET', 'POST'])
@only_owner_can
@login_required
def add_synword(project_id, bot_id):
    form=SynWordForm()
    if form.validate_on_submit():
        b = form.base_word.data 
        s = form.synword.data 
        syn = SynWord(
            base_word=b,
            syn_word=s,
            bot_id=bot_id
        )
        db.session.add(syn)
        db.session.commit()
        flash("新的近义词组添加成功", "success")
        return redirect(url_for('bot.synword', project_id=project_id, bot_id=bot_id))
    return render_template('bot/add_synword.html', form=form, project_id=project_id, bot_id=bot_id)

@bot_bp.route('<int:project_id>/<int:bot_id>/<int:synword_id>/delete_synword', methods=['POST'])
@only_owner_can
@login_required
def delete_synword(project_id, bot_id, synword_id):
    synword = SynWord.query.get_or_404(synword_id)
    db.session.delete(synword)
    db.session.commit()
    flash('该同义词集已删除', 'success')
    return redirect_back()

@bot_bp.route('<int:project_id>/<int:bot_id>/<int:synword_id>/edit_synword', methods=['GET', 'POST'])
@only_owner_can
@login_required
def edit_synword(project_id, bot_id, synword_id):
    synword = SynWord.query.get_or_404(synword_id)

    form = SynWordForm(
        base_word=synword.base_word,
        synword=synword.syn_word)
    form.submit.label.text = "保存"

    if form.validate_on_submit():
        synword.base_word=form.base_word.data
        synword.syn_word=form.synword.data 
        db.session.commit()
        flash('问答对修改成功', 'success')
        return redirect(url_for('bot.synword', project_id=project_id, bot_id=bot_id))
    return render_template('bot/edit_synword.html', project_id=project_id, bot_id=bot_id, synword_id=synword_id, form=form)





@bot_bp.route("<int:project_id>/<int:bot_id>/stopword", methods=['GET','POST'])
@only_owner_can
@login_required
def stopword(project_id, bot_id):
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['QA_PER_PAGE']
    pagination = StopWord.query.filter_by(bot_id=bot_id).paginate(page, per_page=per_page)
    stopword = pagination.items
    return render_template('bot/stopword.html', project_id=project_id, bot_id=bot_id, pagination=pagination, stopword=stopword)

@bot_bp.route('<int:project_id>/<int:bot_id>/add_stopword', methods=['GET', 'POST'])
@only_owner_can
@login_required
def add_stopword(project_id, bot_id):
    form=StopWordForm()
    if form.validate_on_submit():
        s = form.word.data 
        word=re.split(",|，", s)
        for w in word:
            _stopword = StopWord(
                word=w.strip(),
                bot_id=bot_id
            )
            db.session.add(_stopword)
        db.session.commit()
        flash("新的停用词添加成功", "success")
        return redirect(url_for('bot.stopword', project_id=project_id, bot_id=bot_id))
    return render_template('bot/add_stopword.html', form=form, project_id=project_id, bot_id=bot_id)

@bot_bp.route('<int:project_id>/<int:bot_id>/<int:stopword_id>/delete_stopword', methods=['POST'])
@only_owner_can
@login_required
def delete_stopword(project_id, bot_id, stopword_id):
    stopword = StopWord.query.get_or_404(stopword_id)
    db.session.delete(stopword)
    db.session.commit()
    flash('该停用词已删除', 'success')
    return redirect_back()

@bot_bp.route('<int:project_id>/<int:bot_id>/basic_config', methods=['GET', 'POST'])
@only_owner_can
@login_required
def qa_basic_config(project_id, bot_id):
    qabot = QABot.query.filter_by(bot_id=bot_id).first()
    form = QABotBasicForm()
    return render_template('bot/basic_config.html', project_id=project_id, bot_id=bot_id, form=form)