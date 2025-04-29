from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Stock(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    
class Order(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    ORDER_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    order_type = models.CharField(max_length=4, choices=ORDER_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)