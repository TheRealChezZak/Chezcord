from flask import Flask, request
import requests

app = Flask(__name__)

messages = []

@app.route('/send', methods=['POST'])
def receive_message():
    message = request.get_json()['message']
    messages.append(message)
    return "Message received"

@app.route('/receive', methods=['GET'])
def send_message():
    if len(messages) > 0:
        message = messages.pop(0)
        return message
    else:
        return "No messages"

if __name__ == '__main__':
    app.run(debug=True, port=4000)
