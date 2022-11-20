import flask
from flask_socketio import SocketIO, send
import time

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
    send(msg, json=False)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
