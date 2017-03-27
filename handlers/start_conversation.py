from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
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


def weight(bot, update):
    user = update.message.from_user
    logger.info("Weight of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('Good. Now I have all information I need to create your personal diet. '
                              'I`ll send it to you as soon as our professional coaches approve it.')

    return ConversationHandler.END


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

            WEIGHT: [MessageHandler(Filters.text, weight)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler