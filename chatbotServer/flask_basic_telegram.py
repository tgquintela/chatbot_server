#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages.

"""
https://github.com/sooyhwang/Simple-Echo-Telegram-Bot
"""

import os
import sys
import telegram
from flask import Flask, request

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


def create_app(bot, pars):
    ## Paramaters
    TELEGRAM_API_TOKEN = pars['TELEGRAM_API_TOKEN']
#    certified_file = pars['certified_file']
#    certified_file = '/etc/nginx/ssl/cert.pem'
    ## Create app
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    app = Flask(__name__,
                static_folder=static_folder)  # ,

    telegrambot = telegram.Bot(token=TELEGRAM_API_TOKEN)
#    webhook = telegrambot.setWebhook("https://<ip>/telegram/receivemessage",
#                                     cert=open(certified_file, 'rb'))

    @app.route('/HOOK', methods=['POST'])
    def webhook_handler():
        if request.method == "POST":
            # retrieve the message in JSON and
            # then transform it to Telegram object
            update = telegram.Update.de_json(request.get_json(force=True))

            chat_id = update.message.chat.id

            # Telegram understands UTF-8, so encode text for
            # unicode compatibility
            text = update.message.text.encode('utf-8')

            ## Create text answer
            answer = answer = bot.get_message({'message': text})
            answer_text = prepare_message(answer)

            # repeat the same message back (echo)
            telegrambot.sendMessage(chat_id=chat_id, text=answer_text)

        return 'ok'

    @app.route('/set_webhook', methods=['GET', 'POST'])
    def set_webhook():
        s = telegrambot.setWebhook('https://URL/HOOK')
        if s:
            return "webhook setup ok"
        else:
            return "webhook setup failed"

    @app.route('/')
    def index():
        return '.'

    return app


if __name__ == "__main__":
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

    ## Create app
    app = create_app(handler_ui, conf_pars)

    ## Run app
    app.run(debug=True, host='0.0.0.0', port=5000)
