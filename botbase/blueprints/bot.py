from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user

from botbase.models import User, Project, Bot
from botbase.forms import ProjectForm, BotForm
from botbase.extensions import db
from botbase.utils import redirect_back
from botbase.decorators import admin_required, only_owner_can

bot_bp = Blueprint('bot', __name__)

@bot_bp.route("/<int:project_id>/<int:bot_id>", methods=['GET','POST'])
def index(project_id, bot_id):
    return render_template('bot/index.html',project_id=project_id, bot_id=bot_id)

@bot_bp.route("<int:project_id>/<int:bot_id>/qa", methods=['GET','POST'])
def qa(project_id, bot_id):
    pass