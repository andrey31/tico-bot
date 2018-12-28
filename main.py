from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ
import logging
import time


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Bot token in environment variable
TOKEN = environ['TOKEN']


def start_or_help(bot, update):
    '''Send a message when command /start or command /help is issued'''
    update.message.reply_text(
        """Hola.\
\nYo he sido programado para funcionar \
solo en este grupo @grupotelegramcostarica\
        """)


def get_id(bot, update):
    ''' Send a message with group id / user id '''
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    response = f'El id del grupo es: {chat_id}.\nTu id es: {user_id}'

    update.message.reply_text(response)


def welcome(bot, update):
    """Send the welcome message"""

    # telegraph with rules/channels
    telegraph = 'http://telegra.ph/Bienvenida-05-30'

    # convert time server to time Costa Rica
    time_cr = time.time() - (60*(60*6))

    # time Costa Rica format
    time_cr = time.strftime("%I:%M %p", time.localtime(time_cr))

    chat_id = update.message.chat_id
    chat_name = update.message.chat.title

    list_users = update.message.new_chat_members
    count_users = len(list_users)

    message_welcome = ''
    users = ''

    if(count_users == 1):
        message_welcome = '¡Bienvenido/a, '
        dict_user = list_users[0]
        users = dict_user['first_name']
    else:
        message_welcome = '¡Bienvenidos/as, '

        for user in list_users:
            users += user['first_name'] + ', '

    msg = f'{message_welcome} {users} a "{chat_name}" '\
        'por favor  visite las reglas  del grupo '\
        f'y los demás canales que puedan ser de su agrado.\n'\
        f'La hora en Costa Rica es: {time_cr}\n' \
        f'{telegraph}'

    bot.send_message(chat_id=chat_id, text=msg)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_or_help))
    dp.add_handler(CommandHandler("help", start_or_help))
    dp.add_handler(CommandHandler("getid", get_id))
    dp.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
