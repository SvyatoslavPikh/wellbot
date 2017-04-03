from settings import API_KEY
from telegram.ext import Updater, JobQueue, CommandHandler
import logging
from handlers.start_conversation import get_start_conversation_handler


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def info(bot, update):
    update.message.reply_text(
        str(update.message.from_user))


def get_takings(bot, update):
    update.message.reply_text(
        str(update.message.from_user))

logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

updater = Updater(API_KEY)

updater.dispatcher.add_handler(get_start_conversation_handler())
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('debug_info', info))
updater.dispatcher.add_handler(CommandHandler('get_takings', get_takings, pass_job_queue=True))

updater.start_polling()
updater.idle()
