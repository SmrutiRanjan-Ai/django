from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from io import BytesIO
from PIL import Image

# Create your models here.
class ShippingAddress(models.Model):
    class Meta:
        verbose_name = 'ShippingAddress'
        verbose_name_plural = 'ShippingAddresses'

    ShippingAddressId = models.AutoField(primary_key=True)
    ShippingName = models.CharField(max_length=200,null=True,blank=True,default=None)
    ShippingAddressLine1 = models.CharField(max_length=200)
    ShippingAddressLine2 = models.CharField(max_length=200, null=True, blank=True, default=None)
    ShippingAddressState = models.CharField(max_length=50)
    ShippingAddressCity = models.CharField(max_length=50)
    ShippingAddressCountry = models.CharField(max_length=50,default='India')
    ShippingAddressPinCode = models.CharField(max_length=10)
    ShippingAddressPhone = models.BigIntegerField()
    ShippingAddressCustomerId = models.ForeignKey(User, default=None, on_delete=models.CASCADE)