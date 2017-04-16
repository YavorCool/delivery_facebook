import requests
from cfg import PAT

#Запустил скрипт - Сделал кнопку НАЧАТЬ

payload = {
  "get_started": {
      "payload": '{"type": "get_started_button"}'
  }
}

if __name__ == "__main__":
    r = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token=' + PAT, json=payload)
    print(r.text)
