from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from product.models import *


# Create your models here.
class SiteMetaData(models.Model):
    class Meta:
        verbose_name = 'SiteMetaData'
        verbose_name_plural = 'SiteMetaData'

    SiteId = models.AutoField(primary_key=True)
    SiteTitle = models.CharField(max_length=100)
    SiteFlatShipping = models.BooleanField(default=False)
    SiteFlatShippingLimit = models.IntegerField(default=0, blank=True, \
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    SiteIsCODAllowed = models.BooleanField(default=True, blank=True)
    SiteAddressLine1 = models.CharField(max_length=100)
    SiteAddressLine2 = models.CharField(max_length=100)
    SiteShippingAddressState = models.CharField(max_length=50)
    SiteShippingAddressCountry = models.CharField(max_length=50)
    SiteShippingAddressPincode = models.CharField(max_length=10)
    SiteTermsConditions = models.CharField(max_length=1000)
    SiteFacebookLink = models.URLField(blank=True, null=True, default=None)
    SiteTwitterLink = models.URLField(blank=True, null=True, default=None)
    SitePhoneList = models.CharField(max_length=200)
    SiteProducts = models.ManyToManyField(Product, blank=True)


class FileUpload(models.Model):
    class Meta:
        verbose_name = 'FileUpload'
        verbose_name_plural = 'FileUpload'

    FileId = models.AutoField(primary_key=True)
    FileData = models.FileField()
    FileUrl = models.URLField(blank=True, null=True)