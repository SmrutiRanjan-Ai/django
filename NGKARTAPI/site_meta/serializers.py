from rest_framework import serializers
from site_meta.models import *

class SiteMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteMetaData
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'