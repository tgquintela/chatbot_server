#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages.
# This program is dedicated to the public domain under the CC0 license.

"""
app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
webhook = bot.setWebhook("https://<ip>/telegram/receivemessage",
                         cert=open('/etc/nginx/ssl/cert.pem', 'rb'))


@app.route("/receivemessage", methods=['POST'])
def receive_message():
    pass

"""

import sys
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep

from chatbotQuery.ui import HandlerConvesationUI


def prepare_message(messageDict):
    ## Prepare text to show
    if messageDict['collection']:
        speechResponse = []
        for m in messageDict['message']:
            if m['from'] == 'bot':
                speechResponse.append(str(m['message']))
        speechResponse = str('\n'.join(speechResponse))
    else:
        speechResponse = str(messageDict['message'])
    ## Filter and adapt message
    answer = speechResponse
    return answer


def run_app(bot, pars):
    ## Parameters
    TELEGRAM_API_TOKEN = pars['TELEGRAM_API_TOKEN']
    update_id = None

    ## Main route
    bot = telegram.Bot(TELEGRAM_API_TOKEN)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        ## Get only the last message
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    ## Logging
    dateformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=dateformat)

    ## Running loop
    while True:
        try:
            # Request updates after the last update_id
            for update in bot.get_updates(offset=update_id, timeout=10):
                update_id = update.update_id + 1

                # your bot can receive updates without messages
                if update.message:
                    # Get the message text
                    message = update.message.text
                    # Get and format answer
                    answer = bot.get_message({'message': message})
                    answer_text = prepare_message(answer)
                    # Reply to the message
                    update.message.reply_text(answer_text)

        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


if __name__ == '__main__':
    ## Parse parameters
    args = sys.argv
    db_conf_file = args[1]
    conv_conf_file = args[2]
#    parameters_file = args[3]
#
#    with open(parameters_file) as data_file:
#        conf_pars = json.load(data_file)
#    conf_pars = conf_pars if isinstance(conf_pars, dict) else conf_pars[0]
    conf_pars = {}

    ## Parser parameters
    handler_ui = HandlerConvesationUI.\
        from_configuration_files(db_conf_file, conv_conf_file)

    ## Run app
    run_app(handler_ui, conf_pars)
