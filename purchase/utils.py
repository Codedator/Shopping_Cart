import json
from .models import *


def guest_cart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items_selected = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cart_items = order['get_cart_items']

    for p in cart:
        try:
            d_price = 0

            cart_items += cart[p]['quantity']

            item = Item.objects.get(id=p)

            if item.discount_quantity > 0:
                d_price = (cart[p]['quantity'] // item.discount_quantity) * item.discount_amount

            total = ((item.item_price * cart[p]['quantity']) - d_price)

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[p]['quantity']

            item_display = {
                'item': {
                    'id': item.id,
                    'item_name': item.item_name,
                    'item_price': item.item_price,
                },
                'quantity': cart[p]['quantity'],
                'get_item_discount': d_price,
                'get_item_total': total
            }
            items_selected.append(item_display)

        except:
            pass

    return {'cart_items': cart_items, 'order': order, 'items_selected': items_selected}


def cart_purchase(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, cart_status=False)
        items_selected = order.orderitem_set.all()
        cart_items = order.get_cart_items

    else:
        guest_data = guest_cart(request)
        cart_items = guest_data['cart_items']
        order = guest_data['order']
        items_selected = guest_data['items_selected']

    return {'cart_items': cart_items, 'order': order, 'items_selected': items_selected}


def guest_checkout(request, data):
    print("User is not logged in")
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    guest_data = guest_cart(request)

    items = guest_data['items_selected']
    customer, created = Customer.objects.get_or_create(email=email)

    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, cart_status=False)

    for i in items:
        item = Item.objects.get(id=i['item']['id'])
        order_item = OrderItem.objects.create(item=item, order=order, quantity=i['quantity'])

    return customer, order
