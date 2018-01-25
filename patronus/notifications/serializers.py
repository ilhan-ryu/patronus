from rest_framework import serializers
from . import models
from patronus.users import serializers as user_serializers
from patronus.images import serializers as image_serializers

class NotificationSerializer(serializers.ModelSerializer):

    creator = user_serializers.ListUserSerializers()
    image = image_serializers.SmallImageSerializer()
    
    class Meta:
        model = models.Notification
        fields = '__all__'