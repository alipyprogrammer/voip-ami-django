from rest_framework import serializers
from .models import *

class ActiveChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveChannels
        fields = '__all__'


class ForwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forward
        fields = '__all__'


class PeersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peers
        fields = '__all__'








class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'



class Member5040Serializer(serializers.ModelSerializer):
    class Meta:
        model = Member5040
        fields = '__all__'



class MemberFellowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberFellows
        fields = '__all__'












class Peers5040Serializer(serializers.ModelSerializer):
    class Meta:
        model = Peers5040
        fields = '__all__'


class PeersFellowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeersFellows
        fields = '__all__'



