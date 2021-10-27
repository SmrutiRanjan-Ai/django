from django.conf.urls import url
from customer import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'shipaddr/customer/(\d+)/', views.ShippingAddressViewForCustomerId.as_view()),
    url(r'shipaddr/(\d+)/', views.ShippingAddressViewForID.as_view()),
    url(r'shipaddr/', views.ShippingAddressViewList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
