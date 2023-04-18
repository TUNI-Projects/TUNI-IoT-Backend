from .models import data, acc, gyro
from rest_framework.serializers import ModelSerializer


class BasicSerializer(ModelSerializer):

    class Meta:
        model = data
        fields = "__all__"


class AccSerializer(ModelSerializer):

    class Meta:
        model = acc
        fields = "__all__"


class GyroSerializer(ModelSerializer):

    class Meta:
        model = gyro
        fields = "__all__"
