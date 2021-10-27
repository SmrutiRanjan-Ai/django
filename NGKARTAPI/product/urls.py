from django.conf.urls import url
from product import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[

    url(r'product_category/(\w+)/', views.ProductViewForCategory.as_view()),
    url(r'product/(\w+)/', views.ProductViewForIdAndSlug.as_view()),    
    url(r'product/', views.ProductViewList.as_view()),
    url(r'product_latest/(\d+)/', views.LatestProductList.as_view()),
    url(r'product_latest/', views.LatestProductList.as_view()),

    url(r'tax/(\d+)/', views.TaxViewForId.as_view()),
    url(r'tax/', views.TaxViewList.as_view()),

    url(r'tag/(\w+)/', views.TagViewForSlug.as_view()),
    url(r'tag/', views.TagViewList.as_view()),

    url(r'category/(\w+)/', views.CategoryViewForSlug.as_view()),
    url(r'category/', views.CategoryViewList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
