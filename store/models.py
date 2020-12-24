from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    tel1 = models.CharField(max_length=100,blank=True, null=True)
    tel2 = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return self.name

class AnonymousCustomer(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    tel1 = models.CharField(max_length=100,blank=True, null=True)
    tel2 = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return self.name

    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='category_pics', null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(default='product.png', upload_to='product_pics')
    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_opened = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return str(self.order_id)
    

    @property
    def get_cart_items(self):
        all_items = self.orderitem_set.all()
        total = sum([item.quantity for item in all_items])
        return total
    
    
    @property
    def get_cart_total(self):
        all_items = self.orderitem_set.all()
        total = sum([item.get_total for item in all_items])
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    
class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    tel1 = models.CharField(max_length=100,blank=True, null=True)
    tel2 = models.CharField(max_length=100,blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address


