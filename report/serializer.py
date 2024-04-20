from rest_framework import serializers
from .models import Report
from User.serializers import *

from rest_framework import serializers
from .models import Report
from User.serializers import UserSerializer



class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = "__all__"


    

    
