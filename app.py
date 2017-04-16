from flask import Flask, request
import json
import requests
from generic_menu import init_menu, get_menu
from quick_reply_menu import get_quick_reply_menu
from cfg import VERIFY_STRING, PAT
import postback_types, quick_reply_types
from cart import Cart
from products_data import get_product_by_id
from cart_reciept_template import get_cart_receipt_template

app = Flask(__name__)

msg_url = 'https://graph.facebook.com/v2.6/me/messages/?access_token=' + PAT


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
                            send_cart(Cart(sender_id))
                        elif payload['name'] == 'menu':
                            send_menu(sender_id)
                        elif payload['name'] == 'clear_cart':
                            clear_cart(Cart(sender_id))
                            send_text(sender_id, 'Корзина успешно очищена')

                    elif payload['type'] == postback_types.PRODUCTS_MENU_BUTTON:
                        send_quick_reply_menu(sender_id, payload['id'])

                    elif payload['type'] == postback_types.GET_STARTED_BUTTON:
                        send_text(sender_id, 'Нажмите меню для выбора товара')

                elif messaging_event.get('message').get('quick_reply'):
                    print("messaging event:" , messaging_event)
                    payload = json.loads(messaging_event['message']['quick_reply']['payload'])
                    if payload['type'] == quick_reply_types.QR_PROUDCT_COUNT:
                        count = int(messaging_event['message']['text'])
                        add_to_cart(Cart(sender_id), get_product_by_id(payload['id']), count)
                        send_text(sender_id, "Товар успешно добавлен в корзину")
                else:
                    message_text = messaging_event['message']['text']
                    send_text(sender_id, message_text)

    return "OK"


def send_text(recipient, text):
    payload = {'recipient': {'id': recipient}, 'message': {'text': text}}
    r = requests.post(msg_url, json=payload)
    print("Send text post: " + r.text)


def send_menu(recipient):
    payload = {'recipient': {'id': recipient}, 'message': get_menu()}
    r = requests.post(msg_url, json=payload)
    print("Send menu post: " + r.text)


def send_quick_reply_menu(recipient, product_id, count=10):
    r = requests.post(msg_url, json=get_quick_reply_menu(recipient, product_id, count))
    print("Send quick_reply post: " + r.text)


def send_cart(cart):
    r = requests.post(msg_url, json=get_cart_receipt_template(cart))
    print("Sended cart: " + r.text)


def get_cart(user_id):
    return Cart(user_id)


def add_to_cart(cart, product, count):
    for item in cart.items:
        if item['product']['id'] == product['id']:
            item['count'] += count
            cart.write_to_db()
            return item
    item = {"product": product, "count": int(count)}
    cart.items.append(item)
    cart.write_to_db()
    return item


def clear_cart(cart):
    cart.items = []
    cart.write_to_db()


if __name__ == "__main__":
    init_menu()
    app.run(host='0.0.0.0', port='8000')