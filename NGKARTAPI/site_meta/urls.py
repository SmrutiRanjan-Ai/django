from django.conf.urls import url
from site_meta import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'sitemeta/(\d+)/', views.SiteMetadataViewForId.as_view()),
    url(r'sitemeta/(\w+)/', views.SiteMetadataViewForTitle.as_view()),
    url(r'sitemeta/', views.SiteMetaDataViewList.as_view()),

    url(r'fileupload/(\d+)/', views.FileUploadViewForId.as_view()),
    url(r'fileupload/', views.FileUploadViewList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)