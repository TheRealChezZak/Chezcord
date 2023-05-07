from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

port = 4000
messages = []

@app.route('/')
def home():
    return render_template('indexold.html')

@app.route('/receive')
def receive():
    if messages:
        # Check if the first message is valid JSON
        try:
            message = json.loads(messages[0])
            messages.pop(0)
            return jsonify({'message': message})
        except ValueError:
            pass
    
    return jsonify({'message': None})

@app.route('/send', methods=['POST'])
def send_message():
    message = request.form['message']
    messages.append(message)
    socketio.emit('message', {'data': message}, broadcast=True)
    return ''

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    messages.append(message['data'])
    socketio.emit('message', {'data': message['data']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=port, debug=True)
