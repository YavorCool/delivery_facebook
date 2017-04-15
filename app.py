from flask import Flask, request
import json
import requests
from generic_menu import init_menu, get_menu
from cfg import VERIFY_STRING, PAT
import postback_types

app = Flask(__name__)


@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling verification...")
    if request.args.get('hub.verify_token', '') == VERIFY_STRING:
        print("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    print(data)

    if data['object'] == 'page':
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("postback"):
                    message_text = messaging_event["postback"]["payload"]
                    message_text = message_text.lower()
                    sender_id = messaging_event["sender"]["id"]
                    print("message = " + message_text)
                    payload = json.loads(message_text)

                    if payload['type'] == postback_types.PERSISTENT_MENU_BUTTON:
                        if payload['name'] == 'cart':
                            send_text('cart btn pressed', sender_id)
                        elif payload['name'] == 'menu':
                            send_menu(sender_id)

                    elif payload['type'] == postback_types.PRODUCTS_MENU_BUTTON:
                        send_text(payload['id'], sender_id)

                    elif payload['type'] == postback_types.GET_STARTED_BUTTON:
                        send_text('Нажмите меню для выбора товара', sender_id)
                else:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    send_text(message_text, sender_id)
    return "OK"


def send_text(text, recipient):
    payload = {'recipient': {'id': recipient}, 'message': {'text': text}}
    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + PAT, json=payload)
    print(r.text)


def send_menu(recipient):
    print("sending menu...")
    payload = {'recipient': {'id': recipient}, 'message': get_menu()}
    r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + PAT, json=payload)
    print(r.text)


if __name__ == "__main__":
    init_menu()
    app.run(host='0.0.0.0', port='8000')