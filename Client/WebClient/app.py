import flask
from flask_socketio import SocketIO, send
import time
import json

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app)


@app.route('/')
def index():
    return flask.render_template('index.html')


@socketio.on('message')
def handle_messageS(msg):
    print(f'Message: {msg}')
    time.sleep(2)


# TODO: Create a disconnect event handler to logout maybe
@socketio.on('connect')
def handle_connect():
    # Load all messages and send them to the Client
    messages_json = json.dumps(['FETCHED_MESSAGES',
                                [0, 1, 'Some Lorem ipsum messages'],
                                [1, 2, 'Some more lorem messages'],
                                [1, 3, 'More messages from me to 3'],
                                [3, 1, 'Message from 3 to me']])
    send(messages_json, json=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Front end Client disconnected!')

@app.route('/get_my_username')
def username_request():
    return 'flinnfx#101'

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)
