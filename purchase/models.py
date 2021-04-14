from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    item_name = models.CharField(max_length=200, null=True)
    item_price = models.IntegerField(default=0)
    discount_quantity = models.IntegerField(default=0)
    discount_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.CharField(max_length=200, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    cart_status = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_item_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_total_discount(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_item_discount for item in orderitems])
        return total


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.item_name

    @property
    def get_item_total(self):
        return (self.item.item_price * self.quantity) - self.get_item_discount

    @property
    def get_item_discount(self):
        if self.item.discount_quantity == 0:
            return 0
        return (self.quantity // self.item.discount_quantity) * self.item.discount_amount


class ShippingDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pin_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class FinalDiscount(models.Model):
    cart_total = models.IntegerField(default=0, null=True, blank=True)
    discount_amount = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)
