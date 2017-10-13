
"""

References
----------
.. [1] https://chatbotslife.com/build-a-working-sms-chat-bot-in-10-minutes
-b8278d80cc7a

"""

import sys
import json
from flask import Flask
import twilio.twiml
from twilio.rest import TwilioRestClient

from chatbotQuery.ui import HandlerConvesationUI

## Twilio account info
#account_sid = "AC11ba____________________96e87003"
#auth_token = "6789333____________________849d2"
#account_num = "+1617_____42"


def jsonify_message(messageDict):
    if messageDict['collection']:
        answer = []
        for m in messageDict['message']:
            answer.append(str(m['message']))
        answer = str(' '.join(answer))
    else:
        answer = str(messageDict['message'])
    answer = json.loads(answer)
    return answer


def create_app(bot, pars):
    ## Parameters
    account_sid = pars['account_sid']
    auth_token = pars['auth_token']
    account_num = pars['account_num']
    client = TwilioRestClient(account_sid, auth_token)
    SECRET_KEY = pars['SECRET_KEY']

    ## App creation
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route('/hello')
    def hello_world():
        return 'Hello api.ai (from Flask!)'

    @app.route("/", methods=['GET', 'POST'])
    def server():
        from flask import request
        # get SMS input via twilio
        resp = twilio.twiml.Response()

        # get SMS data and metadata
        msg_from = request.values.get("From", None)
        msg = request.values.get("Body", None)

        # Get and format answer
        messageDict = bot.get_message({'message': msg})
        response_obj = jsonify_message(messageDict)

        # Send answer
        if 'result' in response_obj:
            response = response_obj["result"]["fulfillment"]["speech"]
            # send SMS response back via twilio
            client.messages.create(to=msg_from, from_=account_num,
                                   body=response)
        return str(resp)

    return app


if __name__ == "__main__":
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
