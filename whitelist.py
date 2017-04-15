import requests
from cfg import PAT

req = {
  "setting_type" : "domain_whitelisting",
  "whitelisted_domains" : ["https://facebook.com"],
  "domain_action_type": "add"
}

r = requests.post('https://graph.facebook.com/v2.6/me/thread_settings?access_token=' + PAT, json=req)
print(r)