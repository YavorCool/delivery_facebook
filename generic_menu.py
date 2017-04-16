from products_data import product_payload, products

# Формирование меню с продуктами, пока из products_data

menu_elements = []


def init_menu():
    for product in products:
        element = {'title': product['title'],
                   'image_url': product['image_url'],
                   'subtitle': "{} рублей: {}".format(product['price'],product['subtitle'])
                   }

        element['buttons'] = [
            {
                "type": "postback",
                "payload": product_payload % product['id'],
                "title": "В корзину"
            }
        ]
        menu_elements.append(element)


def get_menu():
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": menu_elements
            }
        }
    }

