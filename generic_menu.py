product_payload = '{"type": "products_menu_button",' \
                  '"id": %s}'

products = [{'id': '1',
             'title': 'Гамбургер',
             'image_url': 'https://scontent-arn2-1.xx.fbcdn.net/v/t1.0-9/17904049_749420091898582_7046445455780381383_n.png?oh=44013266a0e4fdb9340b9955366dd98e&oe=598CEBDF',
             'subtitle': 'Бургер с одной котлетой'
             },
            {'id': '2',
             'title': 'Двойной Гамбургер',
             'image_url': 'https://scontent-arn2-1.xx.fbcdn.net/v/t1.0-9/17362479_749420041898587_4204192282191711541_n.jpg?oh=ccdbdb13d59fed49e5e5699a555b54a3&oe=59857ABC',
             'subtitle': 'Бургер с двумя котлетами'
             }
            ,
            {'id': '3',
             'title': 'Пицца салями',
             'image_url': 'https://scontent-arn2-1.xx.fbcdn.net/v/t31.0-8/17973452_749420105231914_3673184004882386026_o.jpg?oh=597075e5a23da5ac747d9185301cc307&oe=59866752',
             'subtitle': 'Сыр, колбаса, соус, помидоры'
             }
            ,
            {'id': '4',
             'title': 'Пицца с ветчиной',
             'image_url': 'https://scontent-arn2-1.xx.fbcdn.net/v/t1.0-9/17862763_749420038565254_8947966646929473572_n.jpg?oh=1b840c9ede076319d73da3e849422456&oe=5994BBED',
             'subtitle': 'Тонкое тесто, сыр, ветчина, грибы'
             }
            ,
            {'id': '5',
             'title': 'Филадельфия',
             'image_url': 'https://scontent-arn2-1.xx.fbcdn.net/v/t1.0-9/17757639_749420045231920_1068338302177148852_n.jpg?oh=a7b79ca37cba5a5f4bb823797b9fa27a&oe=5956BF8C',
             'subtitle': 'Рыба, рис итд итп'
             }
            ]



menu_elements = []


def init_menu():
    for product in products:
        element = {'title': product['title'],
                   'image_url': product['image_url'],
                   'subtitle': product['subtitle']
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

