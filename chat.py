import os
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# We don't need to specify a port here, Flask will automatically use port 5000 by default
messages = []

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    messages.append(message)
    # get the session id of the sender
    sender_id = session.get('client_id')
    # check if the sender is the same as the client who sent the message
    if sender_id != message['id']:
        emit('message', message, broadcast=True)


@app.route('/send', methods=['POST'])
def send_message():
    message = request.form['message']
    username = request.form['username']
    avatar_url = request.form.get('avatar_url', '/static/defava.png')
    message_with_info = {
        'avatar_url': avatar_url,
        'username': username,
        'message': message
    }
    messages.append(message_with_info)
    socketio.emit('message', message_with_info, broadcast=True)
    return jsonify(message_with_info)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # store the client's session id
    session['client_id'] = request.sid

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    socketio.run(app, port=4001)
