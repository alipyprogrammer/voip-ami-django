from rest_framework import serializers
from .models import Report
from User.serializers import *

from rest_framework import serializers
from .models import Report
from User.serializers import UserSerializer
from .views import *




def string_to_list(string):
    try:
        result_list = eval(string)
        if isinstance(result_list, list):
            return result_list
        else:
            raise ValueError("Input is not a valid list string.")
    except Exception as e:
        print("Error:", e)
        return None





class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = "__all__"



    def to_representation(self, instance):
        data = super().to_representation(instance)


        data['queue_log'] = string_to_list(data['queue_log'])
        data['agent'] = string_to_list(data['agent'])

        return data    

