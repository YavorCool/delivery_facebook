from quick_reply_types import QR_PROUDCT_COUNT

payload = '{"type":"' + QR_PROUDCT_COUNT + '", "id": "%s"}'


def get_quick_reply_menu(recipient, product_id, count=10):

    replies = []
    i = 1
    while i <= count:
        reply = {
            "content_type": "text",
            "title": i.__str__(),
            "payload": payload % product_id
                 }
        i += 1
        replies.append(reply)

    request_body = {
      "recipient":{
        "id": "%s"%recipient
      },
      "message": {
        "text": "Выберите количество:",
        "quick_replies":  replies
      }
    }

    return request_body

print(get_quick_reply_menu(0, 2))
