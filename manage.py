import datetime
import logging

from telegram.ext import CommandHandler
from telegram.ext import (Job, Updater, MessageHandler, Filters)

import api
from lib.chatscript import ChatScript
from scheduler import Scheduler

from settings import API_KEY


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


def id(bot, update):
    update.message.reply_text(
        str(update.message.from_user.id))

# logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test(bot, update, job_queue):
    chat_id = update.message.from_user.id
    user_name = update.message.from_user.username
    if not user_name:
        user_name = '%s %s' % (update.message.from_user.first_name, update.message.from_user.last_name)
    menu = scheduler.test(str(chat_id), user_name)
    # for tak in menu.takings:
    #     try:
    #         # if chat_id not in jobs:
    #         job = Job(alarm, (tak.datetime - datetime.datetime.now()).seconds, repeat=False, context=(chat_id, tak.message))
    #         job_queue.put(job)
    #     except Exception as e:
    #         logger.error('[%s] %s' % (chat_id, repr(e)))
    update.message.reply_text('Test takings scheduled')


def alarm(bot, job):
    chat_id = job.context[0]
    message = job.context[1]
    logger.info('[%s] Checking alarm.' % chat_id)

    bot.sendMessage(chat_id, message)


# updater
updater = Updater(API_KEY)

# REST API

api.start(context=updater)

# scheduler
scheduler = Scheduler()

updater.dispatcher.add_handler(MessageHandler(Filters.text, answer))
# updater.dispatcher.add_handler(get_start_conversation_handler())
updater.dispatcher.add_handler(CommandHandler('id', id))
# updater.dispatcher.add_handler(CommandHandler('debug_info', info))
updater.dispatcher.add_handler(CommandHandler('test', test, pass_job_queue=True))

updater.start_polling()
updater.idle()