from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from record.models import ReservationsHamkadeh


class ReservationsHamkadehSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date   = serializers.SerializerMethodField()
    class Meta:
        model = ReservationsHamkadeh
        fields =(  "start_date" , "end_date" , "status" )


    def get_start_date(self, obj):
        return obj.start_date.strftime('%Y-%m-%d %H:%M')


    def get_end_date(self, obj):
        return obj.end_date.strftime('%Y-%m-%d %H:%M')
