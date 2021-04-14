from django.shortcuts import render
from .models import *
from .utils import guest_cart, cart_purchase, guest_checkout
from django.http import JsonResponse
import json
import datetime


# Create your views here.
def item_details(request):

    data = cart_purchase(request)
    cart_items = data['cart_items']

    items = Item.objects.all()
    context = {'items': items, 'cart_items': cart_items}
    return render(request, 'purchase/item_details.html', context)


def shopping_cart(request):

    data = cart_purchase(request)
    cart_items = data['cart_items']
    order = data['order']
    items_selected = data['items_selected']

    context = {'items_selected': items_selected, 'order': order, 'cart_items': cart_items}
    return render(request, 'purchase/shopping_cart.html', context)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def checkout(request):

    data = cart_purchase(request)
    cart_items = data['cart_items']
    order = data['order']
    items_selected = data['items_selected']
    c_total = order['get_cart_total']

    f_discount = FinalDiscount.objects.get(pk=1)
    f_total, add_disc = get_total(f_discount, c_total)
    print(f_total, add_disc)

    context = {'items_selected': items_selected, 'order': order,  'f_total': f_total, 'add_disc': add_disc,
               'cart_items': cart_items}
    return render(request, 'purchase/checkout.html', context)


def get_total(f_discount, c_total):
    if c_total > f_discount.cart_total:
        return c_total-f_discount.discount_amount, f_discount.discount_amount
    return c_total, 0


def update_item(request):
    data = json.loads(request.body)
    item_id = data['itemId']
    action = data['action']
    print(item_id, action)

    customer = request.user.customer
    item = Item.objects.get(id=item_id)
    order, created = Order.objects.get_or_create(customer=customer, cart_status=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)

    if action == 'add':
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        data = json.loads(request.body)
        order, created = Order.objects.get_or_create(customer=customer, cart_status=False)

    else:

        customer, order = guest_checkout(request, data)

    total = int(data['form']['total'])
    order.order_id = transaction_id

    if total == order.get_cart_total:
        order.cart_status = True
    order.save()

    ShippingDetail.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        pin_code=data['shipping']['pincode'],
    )

    return JsonResponse("Payment complete.", safe=False)
