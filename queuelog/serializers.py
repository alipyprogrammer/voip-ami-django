from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class QueueLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueLog
        fields =("idd",)

class QueueLoghamkadehSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueLoghamkadeh
        fields =("idd",)
