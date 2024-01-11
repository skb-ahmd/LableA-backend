from django.db import models
from django.contrib.auth.models import User 

class Product(models.Model):
	name=models.CharField(max_length=255)
	manufacturer=models.CharField(max_length=255)
	price=models.DecimalField(max_digits=10, decimal_places=2)
	available_quantity=models.PositiveIntegerField()
	image_data = models.TextField(null=True, blank=True)

def __str__(self):
	return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product}"
    
class Order(models.Model):
    delivery_time = models.DateTimeField()
    cart_items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)


