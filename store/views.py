from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView
from .models import (Category, Product, Order, OrderItem, Shipping)
from django.contrib import messages
import datetime
from django.utils import timezone


class HomePage(ListView):
    model = Category

class Products(ListView):
    model = Product

class ProductDetail(DetailView):
    model = Product

def category_view(request,id):
    category = Category.objects.get(id=id)
    category_products = Product.objects.filter(category=category)
    context = {
        'products':category_products,
        'title':category.name
    }
    return render(request, 'store/category_products.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete=False)
        # الأوردر لما يكون المستخدم هو اليوزر الحالي
        the_order = Order.objects.get(customer=customer, complete=False)
        # المنتجات لما يكون الأوردر بتاعها هو الأوردر المطلوب
        items = OrderItem.objects.filter(order=the_order)
    else:
        the_order = {
            'get_cart_items':0,
            'get_cart_total':0
        }
        items = []
        # Getting the cookie cart..
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        
        for i in cart:
            the_order['get_cart_items'] += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (cart[i]['quantity'] * product.price)
            the_order['get_cart_total'] += total
            # setting the product
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':{
                        'url':product.image.url
                    }
                },
                'quantity':cart[i]['quantity'],
                'get_total':(product.price * cart[i]['quantity']) 
            }

            items.append(item)
        
    context = {'items':items, 'order':the_order, 'title': 'سلة المشتروات'}
    return render(request, 'store/cart.html', context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # الأوردر لما يكون المستخدم هو اليوزر الحالي
        the_order = Order.objects.get(customer=customer, complete=False)
        # المنتجات لما يكون الأوردر بتاعها هو الأوردر المطلوب
        items = OrderItem.objects.filter(order=the_order)
    else:
        the_order = {
            'get_cart_items':0,
            'get_cart_total':0
        }
        items = []
       
    context = {'items':items, 'order':the_order, 'title': 'تأكيد المشتروات'}

    return render(request, 'store/checkout_detail.html',context)
  

# The view that updatescart
@csrf_protect
def update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)  
    orderitem, created = OrderItem.objects.get_or_create(product=product, order=order)
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()
        messages.warning(request, 'تم حذف المنتج')
    return JsonResponse('Item was added!', safe=False)

@csrf_protect
def confirm_order(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer=customer, complete=False)
        order.order_id = datetime.datetime.now().timestamp()
        shipping, created = Shipping.objects.get_or_create(
            customer=customer,
            order=order,
            address=customer.address,
            city=customer.city,
            state=customer.state,
            tel1=customer.tel1,
            tel2=customer.tel2,
        )
        
        
    else:
        customer = data['userData']['username']
        order, created = Order.objects.get_or_create(customer=customer, complete=False, order_id= datetime.datetime.now().timestamp())
        shipping, created = Shipping.objects.get_or_create(
            customer=customer,
            order=order,
            tel1=data['userData']['tel1'],
            address=data['userData']['address'],
            city=data['shippingInfo']['city'],
            state=data['shippingInfo']['state'],
            tel2=data['shippingInfo']['tel2'],
        )
    order.complete = True
    order.save()
    shipping.save()
    return JsonResponse('Order Confirmed.. ', safe=False)

def confirmRedirect(request):
    return render(request, 'store/done.html', {'title':'نجاح العملية'})