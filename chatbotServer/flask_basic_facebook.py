
"""

References
----------
.. [1] https://chatbotnewsdaily.com/build-a-facebook-messenger-chat-bot-in-
10-minutes-5f28fe0312cd

https://github.com/enginebai/PyMessager/blob/master/api.py

"""

import sys
import json
import requests
from flask import Flask, request

from chatbotQuery.ui import HandlerConvesationUI

# FB messenger credentials
ACCESS_TOKEN = ""
base_token_fbpage = "https://graph.facebook.com/v2.6/me/messages?access_token="


def jsonify_message(messageDict):
    if messageDict['collection']:
        answer = []
        for m in messageDict['message']:
            answer.append(str(m['message']))
        answer = str('\n'.join(answer))
    else:
        answer = str(messageDict['message'])
    answer = json.loads(answer)
    return answer


def create_app(bot, pars):
    ## Parameters
    ACCESS_TOKEN = pars['ACCESS_TOKEN']
    SECRET_KEY = pars['SECRET_KEY']

    ## App creation
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = SECRET_KEY

    ## Check request
    @app.route('/', methods=['GET'])
    def verify():
        # our endpoint echos back the 'hub.challenge' value specified
        # when we setup the webhook
        ifsubscribed = request.args.get("hub.mode") == "subscribe"
        if ifsubscribed and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == 'foo':
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200
        return 'Hello World (from Flask!)', 200

    ## Reply function
    def reply(user_id, msg):
        data = {
            "recipient": {"id": user_id},
            "message": {"text": msg}
        }
        resp = requests.post(base_token_fbpage + ACCESS_TOKEN, json=data)
        print(resp.content)

    ## Answer creation
    @app.route('/', methods=['POST'])
    def handle_incoming_messages():
        # Get message
        data = request.json
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']

        # Get and format answer
        messageDict = bot.get_message({'message': message})
        response_obj = jsonify_message(messageDict)

        # Send answer
        if 'result' in response_obj:
            response = response_obj["result"]["fulfillment"]["speech"]
            reply(sender, response)
        return "ok"

    return app


if __name__ == '__main__':
    ## Parse parameters
    args = sys.argv
    db_conf_file = args[1]
    conv_conf_file = args[2]
    parameters_file = args[3]

    with open(parameters_file) as data_file:
        conf_pars = json.load(data_file)
    conf_pars = conf_pars if isinstance(conf_pars, dict) else conf_pars[0]

    ## Create bot
    handler_ui = HandlerConvesationUI.\
        from_configuration_files(db_conf_file, conv_conf_file)

    ## Create app
    app = create_app(handler_ui, conf_pars)

    ## Run app
    app.run(debug=True)
