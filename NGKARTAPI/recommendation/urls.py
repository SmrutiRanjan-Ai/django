from django.conf.urls import url
from recommendation import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[

    url(r'recommend_products/(\w+)/', views.RecommendProductView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)