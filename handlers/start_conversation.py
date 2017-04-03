from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, Job, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
logger = logging.getLogger(__name__)

AGE, WEIGHT = range(2)


def start(bot, update):
    reply_keyboard = [['<20', '20-30', '30-40', '40-50', '>50']]

    update.message.reply_text(
        'Hi! I`m wellness bot. I can create a personal diet for you.'
        'Send /cancel to stop talking to me.\n\n'
        'First of all, I need some infomation about you. '
        'How old are you?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return AGE


def age(bot, update):
    user = update.message.from_user
    logger.info("Age of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('What is your weight?',
                              reply_markup=ReplyKeyboardRemove())

    return WEIGHT


def weight(bot, update, job_queue):
    user = update.message.from_user
    logger.info("Weight of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('Good. Now I have all information I need to create your personal diet. '
                              'I`ll send it to you as soon as our professional coaches approve it.')

    chat_id = update.message.chat_id
    logger.info('[%s] Adding job.' % chat_id)

    try:
        # if chat_id not in jobs:
        job = Job(alarm, 30, repeat=False, context=(chat_id, "Other"))
        job_queue.put(job)
    except Exception as e:
        logger.error('[%s] %s' % (chat_id, repr(e)))

    return ConversationHandler.END


def alarm(bot, job):
    chat_id = job.context[0]
    message = job.context[1]
    logger.info('[%s] Checking alarm.' % chat_id)

    bot.sendMessage(chat_id, message)


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def get_start_conversation_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            AGE: [RegexHandler('^(<20|20-30|30-40|40-50|>50)$', age)],

            WEIGHT: [MessageHandler(Filters.text, weight, pass_job_queue=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler
