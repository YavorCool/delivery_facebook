import requests
from cfg import PAT
import postback_types


CART_PAYLOAD = '{"type": "%s", "name": "cart"}' % postback_types.PERSISTENT_MENU_BUTTON
MENU_PAYLOAD = '{"type": "%s", "name": "menu"}' % postback_types.PERSISTENT_MENU_BUTTON
CLEAR_CART_PAYLOAD = '{"type": "%s", "name": "clear_cart"}' % postback_types.PERSISTENT_MENU_BUTTON

request_payload = {
              "setting_type": "call_to_actions",
              "thread_state": "existing_thread",
              "call_to_actions": [
               {
                "type": "postback",
                "title": "Меню",
                "payload": MENU_PAYLOAD
               },
               {
                 "type": "postback",
                 "title": "Корзина",
                 "payload": CART_PAYLOAD
               },
               {
                 "type": "postback",
                 "title": "Очистить корзину",
                 "payload": CLEAR_CART_PAYLOAD
               },

              ]
             }

if __name__ == "__main__":
    print(request_payload)
    r = requests.post('https://graph.facebook.com/v2.6/me/thread_settings?access_token=' + PAT, json=request_payload)
    print(r.text)
