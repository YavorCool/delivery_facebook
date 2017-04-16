
def get_cart_receipt_template(cart):
    elements = []
    total_cost = 0
    for item in cart.items:
        total_cost += int(item['product']['price']) * item['count']
        element = {
            "title":item['product']['title'],
            "subtitle":item['product']['subtitle'],
            "quantity":item['count'],
            "price":item['product']['price'],
            "currency":"RUB",
            "image_url": item['product']['image_url']
          }
        elements.append(element)

    msg = {
        "recipient": {
            "id": cart.user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": "Stephane Crozatier",
                    "order_number": "12345678902",
                    "currency": "USD",
                    "payment_method": "Visa 2345",
                    "elements": elements,
                    "summary": {
                        "total_cost": total_cost
                    },
                }
            }
        }
    }
    return msg