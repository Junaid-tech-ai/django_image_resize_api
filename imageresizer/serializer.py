from rest_framework import serializers
from .models import UploadedImage, UserVisit


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('id', 'user', 'image', 'timestamp')


class UserVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVisit
        fields = '__all__'
