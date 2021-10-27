from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from io import BytesIO
from PIL import Image

# Create your models here.
class Tax(models.Model):
    TaxId = models.AutoField(primary_key=True)
    TaxName = models.CharField(max_length=50)
    TaxRate = models.IntegerField(default=0, blank=True,\
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    TaxSlug = models.SlugField(default=None)
    def __str__(self):
        return self.TaxName+' @ '+str(self.TaxRate)+'%'
    
    class Meta:
        verbose_name_plural = 'Taxes'
        unique_together = ('TaxName', 'TaxRate')

class Tag(models.Model):
    TagSlug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.TagSlug

    def clean(self):
        self.TagSlug = self.TagSlug.capitalize()


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    
    CategorySlug = models.SlugField(primary_key=True)
    CategoryDescription = models.CharField(max_length=500, null=True, blank=True, default=None)
    CategoryFeaturedImageFile = models.ImageField(null=True, blank=True, default=None)
    CategoryImageUrl = models.CharField(max_length=200,null=True, blank=True, default=None)
    CategoryParent = models.ForeignKey('self', null=True, default=None, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.CategorySlug

    def get_absolute_url(self):
        return f'/{self.CategorySlug}/'
    
    def clean(self):
        self.CategorySlug = self.CategorySlug.capitalize()


class Product(models.Model):
    UNIT_CHOICES = (
        ('KG', 'KG'),
        ('CM', 'CM'),
        ('PC', 'PIECES'),
    )
    BASE_URL = 'http://127.0.0.1.8000'

    ProductId = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=100, blank=True)
    ProductSlug = models.SlugField(max_length=100,unique=True, blank=True)
    ProductDescription = models.TextField(null=True, blank=True)
    ProductFeaturedImageFile = models.ImageField(upload_to='static/product/', null=True, blank=True, default=None)
    ProductIsCustomizable = models.BooleanField(default=False, blank=True)
    ProductPrice = models.DecimalField(validators=[MinValueValidator(0)], max_digits=8, decimal_places=2, blank=True)
    ProductLaunchDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ProductInventory = models.PositiveIntegerField(default=0, blank=True)
    ProductInventoryUnit = models.CharField(max_length=20, choices=UNIT_CHOICES, default=UNIT_CHOICES[0][0])
    ProductCreater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ProductFeaturedPrice = models.PositiveIntegerField(default=0, blank=True)
    ProductDiscountPercentage = models.IntegerField(default=0, blank=True,\
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    ProductShippingRate = models.IntegerField(default=0, blank=True,\
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    ProductFlatShipping = models.BooleanField(default=False, blank=True)
    ProductTaxCode = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)
    ProductCategories = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    ProductTags = models.CharField(max_length=200,blank=True,null=True)
    ProductImageUrl=models.CharField(max_length=200, blank=True)




    class Meta:
        ordering = ['-ProductLaunchDate']

    def __str__(self):
        return '%s has %d %s left' %(self.ProductName, self.ProductInventory, self.ProductInventoryUnit)
    
    def get_image(self):
        if self.image:
            return self.BASE_URL + self.ProductFeaturedImageFile.url
        return ''

