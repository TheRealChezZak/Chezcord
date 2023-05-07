import requests

username = input("Username: ")
password = input("Password: ")
receiver = input("Receiver: ")
message = input("Message: ")

response = requests.post('http://localhost:4000/send',
                         auth=(username, password),
                         json={'receiver': receiver, 'message': message})

print(response.text)
