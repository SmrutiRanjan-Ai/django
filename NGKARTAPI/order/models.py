from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files import File
from io import BytesIO
from PIL import Image
from product.models import *
from customer.models import *

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ('PROCESSING', 'PROCESSING'),
        ('CONFIRMED', 'CONFIRMED'),
        ('PENDING', 'PENDING'),
        ('CANCELLED', 'CANCELLED'),
        ('SHIPPED', 'SHIPPED'),
    )

    OrderId = models.AutoField(primary_key=True)
    OrderShippingRate = models.IntegerField(default=0, blank=True,\
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    OrderFlatShipping = models.BooleanField(default=False, blank=True)
    OrderCustomerId = models.ForeignKey(User, on_delete=models.CASCADE)
    OrderDateTime = models.DateTimeField(auto_now_add=True)
    OrderStatus = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    OrderShippingAddress = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, default=None, null=True)
    OrderTotal = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    OrderTrackingId = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['OrderDateTime']


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'OrderItem'

    OrderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    ProductQuantity = models.PositiveIntegerField()
    ProductTotalCost = models.DecimalField(validators=[MinValueValidator(0)],\
                                                    max_digits=8, decimal_places=2, default=0, blank=True)
    ProductCustomizableImage = models.ImageField(upload_to='static/order/', null=True, blank=True, default=None)
    ProductCustomizableText = models.CharField(max_length=200, blank=True, null=True, default=None)
