from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import QueueLog


class QueueLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueLog
        fields =("idd",)