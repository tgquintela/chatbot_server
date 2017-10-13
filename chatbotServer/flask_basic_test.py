
import time
import sys
import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from chatbotQuery.ui import HandlerConvesationUI


def filter_message(messageDict):
    filtered_fields = ["answer_status", "collection", "from", "posting_status",
                       "sending_status", "message"]
    answer = {}
    for field in filtered_fields:
        if field == "message":
            if isinstance(messageDict['message'], list):
                new_message = []
                for m in messageDict['message']:
                    if m['from'] == 'bot':
                        new_message.append(filter_message(m))
                answer['message'] = new_message
            else:
                answer['message'] = messageDict['message']
        else:
            if field in messageDict:
                answer[field] = messageDict[field]
    return answer


def jsonify_message(messageDict):
#    answer =\
#        {
#            "currentNode": "",
#            "complete": None,
#            "context": {},
#            "parameters": [],
#            "extractedParameters": {},
#            "speechResponse": "ECHO",
#            "intent": {},
#            "input": "init_conversation",
#            "missingParameters": []
#        }
#    return answer
#    return {'status': 'OK', 'answer': messageDict}
#    return {'status': 'OK', 'answer': str(messageDict)}
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
    answer = filter_message(messageDict)
    answer['speechResponse'] = speechResponse
    answer['status'] = 'OK'
    return answer


def create_app(bot, pars):
    ## Create app
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    app = Flask(__name__,
                static_folder=static_folder)  # ,
#                template_folder='templates')
#    CORS(app)

    ## Main route
    @app.route("/")
    def index():
        #{{ url_for('static', filename='js/chatbot_flask.js') }}
        return render_template("testing_chat.html")

    # Request Handler
    @app.route('/api/v1', methods=['POST'])
    def api():
        requestJson = request.get_json(silent=True)
        message = str(requestJson['input'])
        # Get message
        if (message == "quit") or (message is None):
            time.sleep(60)
            exit()

        if message is not None:
            # Get and format answer
            answer = bot.get_message({'message': message})
            if (answer is None):
#                return jsonify({'status': 'OK', 'answer': 'FAILAZO'})
                time.sleep(60)
                exit()

            # Send answer
            response_obj = jsonify(jsonify_message(answer))
            return response_obj

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
