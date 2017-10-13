
import time
import sys
import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit

from chatbotQuery.ui import HandlerConvesationUI


def jsonify_message(messageDict):
    return {'status': 'OK', 'answer': str(messageDict)}
#    if messageDict['collection']:
#        answer = []
#        for m in messageDict['message']:
#            answer.append(str(m['message']))
#        answer = str('\n'.join(answer))
#        return {'status': 'OK', 'answer': answer}
#    else:
#        answer = str(messageDict['message'])
#        return {'status': 'OK', 'answer': answer}


def create_app(bot, pars):
    ## Create app
    static_folder = os.path.join(os.path.dirname(__file__), 'assets')
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder='assets/templates')
#    CORS(app)
    socketio = SocketIO(app)

    ## Main route
    @app.route("/")
    def index():
        return render_template("chat_simple_socket.html")

#    ## Check request
#    @app.route('/', methods=['GET'])
#    def verify():
#        # check correct message
#        if request.form['messageText'] is None:
#            return "Not message", 403
#        return 'Correct message.', 200

#    @app.route("/ask", methods=['POST'])
#    def ask():
#        # Get message
##        message = str(request.json['message'])
#        message = str(request.form['messageText'])
#        if (message == "quit") or (message is None):
#            time.sleep(60)
#            exit()
#
#        if message is not None:
#            # Get and format answer
#            answer = handler_ui.get_message({'message': message})
#            if (answer is None):
#                return jsonify({'status': 'OK', 'answer': 'FAILAZO'})
#                #time.sleep(60)
#                #exit()
#
#            # Send answer
#            response_obj = jsonify(jsonify_message(answer))
#            return response_obj

    @socketio.on('message')
    def handle_message(message):
        if message is not None:
            # Get and format answer
            answer = handler_ui.get_message({'message': message})
            if (answer is None):
                send(jsonify({'status': 'OK', 'answer': 'FAILAZO'}),
                     namespace='/chat')
#                #time.sleep(60)
#                #exit()

            # Send answer
            response_obj = jsonify(jsonify_message(answer))
            send(response_obj, namespace='/chat')

    return socketio, app


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
    socketio, app = create_app(handler_ui, conf_pars)

    ## Run app
    socketio.run(app, host='0.0.0.0', port=5000)
#    app.run(debug=True, host='0.0.0.0', port=5000)
