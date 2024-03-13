from rest_framework import serializers
from .models import UserVisit, ImageModel


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    # width_cm = serializers.FloatField(required=False)
    # height_cm = serializers.FloatField(required=False)
    width_px = serializers.IntegerField(required=False)
    height_px = serializers.IntegerField(required=False)
    # filename = serializers.CharField(required=False)
    format = serializers.CharField(required=False)
    # crop_left = serializers.IntegerField(required=False)
    # crop_top = serializers.IntegerField(required=False)
    # crop_right = serializers.IntegerField(required=False)
    # crop_bottom = serializers.IntegerField(required=False)

    def validate(self, data):
        if 'format' in data:
            image_format = data['format']
            if image_format.lower() == 'jpg' or image_format.lower() == 'jpeg':
                data['format'] = 'JPEG'
            elif image_format.lower() == 'png':
                data['format'] = 'PNG'
        return data


class UserVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVisit
        fields = '__all__'


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['title', 'image']  # Add other fields if necessary

    # If additional validation or customization is needed, you can override the create method
    def create(self, validated_data):
        return ImageModel.objects.create(**validated_data)
