from rest_framework import serializers
from ..models import data, device


class deviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = device
        fields = '__all__'


class dataSerializers(serializers.ModelSerializer):
    class Meta:
        model = data
        fields = '__all__'
