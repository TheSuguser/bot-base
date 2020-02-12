import os

from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory, send_file
from flask_login import login_required, current_user

# from botbase.models import User, Project, Bot
# from botbase.forms import ProjectForm, BotForm, ProjectConfigForm
# from botbase.extensions import db
# from botbase.utils.flask_tool import redirect_back
# from botbase.utils.create_bot import create_qa_bot
# from botbase.decorators import admin_required, only_owner_can

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/<int:project_id>')
def chat(project_id):
    return render_template('chat/chat.html')