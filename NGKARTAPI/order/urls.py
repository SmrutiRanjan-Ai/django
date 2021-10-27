from django.conf.urls import url
from order import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'orders_user/(\d+)/', views.OrderViewForUserId.as_view()),
    url(r'order/(\d+)/', views.OrderViewForId.as_view()),
    url(r'order/', views.OrderViewList.as_view()),

    url(r'order_items/(\d+)/', views.OrderItemViewListForOrderId.as_view()),
    url(r'order_items/', views.OrderItemViewList.as_view()),

    url(r'order_item/(\d+)/(\d+)/', views.OrderItemReadDeleteView.as_view()),
    url(r'order_item/(\d+)/', views.OrderItemCreateReadUpdateView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)