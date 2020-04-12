import os
import sys

from telegram.ext import Updater, MessageHandler, Filters
import requests

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Unfortunately, telegram bots can not read messages from other telegram bots
# Therefore, the matrix and IRC stuff flipbot posts in our channel is not being relayed.
# Fix me by using Matrix or IRC api instead of telegram.


def handle_incoming_message(bot, update):
    logging.debug(update.effective_chat)
    msg = update.message
    # check for t.me/flipdot_kassel, but we will use the id in case it changes
    if update.effective_chat.id != -1001162206905:
        bot.send_message(chat_id=update.effective_chat.id, text='Error occurred while processing message')
        return
    user = msg.from_user.username or msg.from_user.first_name
    logging.info(f'Relaying to mc.flipdot.org: "{user}: {msg.text}"')
    requests.post('http://minecraft.flipdot.org:8123/up/sendmessage', json={
        'name': user, # seens like it doesn't get displayed ingame
        'message': f'{user}: {msg.text}',
    })


def main():
    if 'TELEGRAM_TOKEN' not in os.environ:
        logging.error('You need to set the environment variable "TELEGRAM_TOKEN"')
        return sys.exit(-1)
    updater = Updater(token=os.environ.get('TELEGRAM_TOKEN'))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_incoming_message))

    updater.start_polling()


if __name__ == '__main__':
    main()
