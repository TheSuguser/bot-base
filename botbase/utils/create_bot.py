from flask import current_app

from botbase.models import QABot, Bot
from botbase.extensions import db


def create_qa_bot(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    qabot = QABot(
        name=bot.name,
        lang=bot.lang,
        bot_id = bot.id,
        project_id=bot.project_id,
        user_id = bot.user_id,
        th1 = current_app.config.get('TH1'),
        th2 = current_app.config.get('TH2'),
        k1 = current_app.config.get('K1'),
    )
    db.session.add(qabot)
    db.session.commit()

