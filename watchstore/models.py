# store/models.py
from django.db import models

class UserAccount(models.Model):
    username = models.CharField(max_length=150)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return self.username or f"UserAccount-{self.pk}"

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ShoppingCart(models.Model):
    # user is nullable to support guest carts
    user = models.ForeignKey(UserAccount, related_name="cart_items", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, related_name="cart_entries", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"CartItem: {self.product.title} x {self.quantity}"

class CustomerOrder(models.Model):
    user = models.ForeignKey(UserAccount, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.TextField()
    contact_number = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=15)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.contact_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} x {self.quantity} (Order {self.order.pk})"
