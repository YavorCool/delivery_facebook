from flask import Flask, request
import json
import requests
from generic_menu import init_menu, get_menu
from quick_reply_menu import get_quick_reply_menu
from cfg import VERIFY_STRING, PAT
import postback_types, quick_reply_types

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
                sender_id = messaging_event["sender"]["id"]
                if messaging_event.get("postback"):
                    message_text = messaging_event["postback"]["payload"]
                    message_text = message_text.lower()
                    payload = json.loads(message_text)

                    if payload['type'] == postback_types.PERSISTENT_MENU_BUTTON:
                        if payload['name'] == 'cart':
                            send_text(sender_id, 'cart btn pressed')
                        elif payload['name'] == 'menu':
                            send_menu(sender_id)

                    elif payload['type'] == postback_types.PRODUCTS_MENU_BUTTON:
                        send_quick_reply_menu(sender_id, payload['id'])

                    elif payload['type'] == postback_types.GET_STARTED_BUTTON:
                        send_text(sender_id, 'Нажмите меню для выбора товара')

                elif messaging_event.get('message').get('quick_reply'):
                    print("messaging event:" , messaging_event)
                    payload = json.loads(messaging_event['message']['quick_reply']['payload'])
                    if payload['type'] == quick_reply_types.QR_PROUDCT_COUNT:
                        count = messaging_event['message']['text']
                        send_text(sender_id, "product id: {}, count : {}".format(payload['id'], count))

                else:
                    message_text = messaging_event['message']['text']
                    send_text(sender_id, message_text)

    return "OK"


def send_text(recipient, text):
    payload = {'recipient': {'id': recipient}, 'message': {'text': text}}
    r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + PAT, json=payload)
    print("Send text post: " + r.text)


def send_menu(recipient):
    payload = {'recipient': {'id': recipient}, 'message': get_menu()}
    r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + PAT, json=payload)
    print("Send menu post: " + r.text)


def send_quick_reply_menu(recipient, product_id, count=10):
    payload = get_quick_reply_menu(recipient, product_id, count)
    r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + PAT, json=payload)
    print("Send quick_reply post: " + r.text)

if __name__ == "__main__":
    init_menu()
    app.run(host='0.0.0.0', port='8000')