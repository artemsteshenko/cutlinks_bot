TOKEN = '5222080467:AAGyE02fYaor0H2cqaxMXD-Yjn32vwak7AY'

import os
import uuid
import json
import urllib
import requests
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext, MessageHandler, Filters
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 443))


MENU, SEND_LINK, ASK_LINK = range(3)
GET_LINK, RETURN_MENU, SUB_PREMIUN = range(3)


def shorten_link(link):
    key = 'b8c6c6db7398af334f87720ca667a690dfbb3'
    # link = 'https://ru.wikipedia.org/wiki/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9_%D0%90%D1%84%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D0%BC%D0%BE%D1%80%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D0%BE%D1%8E%D0%B7#%D0%90%D1%84%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F_%D0%B8%D0%BC%D0%BF%D0%B5%D1%80%D0%B8%D1%8F_(454%E2%80%94404_%D0%B3%D0%B3._%D0%B4%D0%BE_%D0%BD._%D1%8D.)'
    url = urllib.parse.quote(link)
    hash = uuid.uuid4().hex[:4]
    hostname = urllib.parse.urlparse(link).hostname

    if hostname is None:
        return 'Необходимо отправить действительную ссылку'

    hostname = hostname.split('.')[-2]
    name = f'{hostname}-{hash}'

    r = requests.get('http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(key, url, name))
    short_link = json.loads(r.text)['url']['shortLink']
    return short_link


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("Получить короткую ссылку", callback_data=str(GET_LINK)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Приыет! Вы можете отправить мне ссылку, а я сделаю ее короче!", reply_markup=reply_markup)
    return ASK_LINK


def menu(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""

    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Получить короткую ссылку", callback_data=str(GET_LINK)),],
        [InlineKeyboardButton("Подписаться на PREMIUM", callback_data=str(SUB_PREMIUN)),]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot = Bot(token=TOKEN)
    bot.sendMessage(chat_id=query.message.chat.id, text='Подписка на PREMIUM\n'
                              '- статистика по переходам\n'
                              '- возможность называть ссылки как угодно\n'
                              '- на ссылку так же можно получить QR код', reply_markup=reply_markup)
    return ASK_LINK


def shortlink_ask(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    bot = Bot(token=TOKEN)
    bot.sendMessage(chat_id=query.message.chat.id, text='Отправьте ссылку')
    return SEND_LINK


def shortlink_send(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    keyboard = [
        [
            InlineKeyboardButton("Вернуться в меню", callback_data=str(RETURN_MENU)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(shorten_link(update.message.text), reply_markup=reply_markup)
    return MENU


def main() -> None:
    """Run the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                CallbackQueryHandler(menu, pattern='^' + str(RETURN_MENU) + '$'),

            ],
            ASK_LINK: [
                CallbackQueryHandler(shortlink_ask, pattern='^' + str(GET_LINK) + '$'),
            ],
            SEND_LINK: [
                MessageHandler(Filters.text & ~Filters.command, shortlink_send)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://sleepy-island-02101.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
