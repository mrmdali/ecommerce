from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from . utils import cartData, guestOrder

from paycomuz.views import MerchantAPIView
from paycomuz.methods_subscribe_api import Paycom

class CheckOrder(Paycom):
    def check_order(self, amount, account):
        return self.ORDER_FOUND

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder


from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz

class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: str):
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        print(order_id)

class TestViewClick(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment

def store(request):
    product = Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId: ', productId)
    print('action: ', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, create = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, create = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)


    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAdress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complate', safe=False)