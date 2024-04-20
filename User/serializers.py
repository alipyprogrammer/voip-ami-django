from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from record.models import ReservationsHamkadeh

class ExpertPhoneSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields =['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'


class UserSeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','name', 'phoneNumber', 'phoneNumber2']

class UserSerializerWithToken(UserSerializer):
    token  =  serializers.SerializerMethodField(read_only =True)
    # status  =  serializers.SerializerMethodField(read_only =True)

    class Meta:
        model =User
        fields =['id','username' ,'email', 'name'  ,'token' ]
    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    # def get_status(self,obj):
    #     status =obj.status

    #     return status

class UserSerializerReport(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id']
