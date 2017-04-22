from settings import API_KEY
from telegram.ext import Updater, JobQueue, CommandHandler
import logging
import threading
from api.server import ApiServer
from handlers.start_conversation import get_start_conversation_handler
from telegram.ext import (Updater, MessageHandler, Filters)
from lib.chatscript import ChatScript
# from utils.db import init_db


def answer(bot, update):
    chat_script = ChatScript()
    answer = chat_script.send_message(update.message.from_user.id, 'HARRY', update.message)
    update.message.reply_text(str(answer))


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def info(bot, update):
    update.message.reply_text(
        str(update.message.from_user))


def get_takings(bot, update, queue):
    update.message.reply_text(
        str(update.message.from_user))


# logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# db
# init_db()

# updater
updater = Updater(API_KEY)

# REST API
api_server = ApiServer()
api_server.start(updater)


updater.dispatcher.add_handler(MessageHandler(Filters.text, answer))
# updater.dispatcher.add_handler(get_start_conversation_handler())
# updater.dispatcher.add_handler(CommandHandler('hello', hello))
# updater.dispatcher.add_handler(CommandHandler('debug_info', info))
# updater.dispatcher.add_handler(CommandHandler('get_takings', get_takings, pass_job_queue=True))

updater.start_polling()
updater.idle()