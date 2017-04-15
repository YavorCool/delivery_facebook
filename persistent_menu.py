import requests
import curl
from cfg import PAT
import postback_types


CART_PAYLOAD = '{"type": %s, "name": "cart"}' % postback_types.PERSISTENT_MENU_BUTTON
MENU_PAYLOAD = '{"type": %s, "name": "menu"}' % postback_types.PERSISTENT_MENU_BUTTON


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
              ]
             }

if __name__ == "__main__":
    r = requests.post('https://graph.facebook.com/v2.6/me/thread_settings?access_token=' + PAT, json=request_payload)
    print(r.text)
