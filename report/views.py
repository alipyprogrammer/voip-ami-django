from django.shortcuts import render
from queuelog.models import *
from django.http import HttpResponse
from .call_log import *
import pandas as pd
import json
from django.shortcuts import render
from itertools import product
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import  api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView ,
    ListAPIView,

    RetrieveAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.generics import get_object_or_404
from .models import *
from .serializer import *
from User.permissions import *
from rest_framework.response import Response
from rest_framework import status
from io import BytesIO



def string_to_list(string):
    try:
        result_list = eval(string)
        if isinstance(result_list, list):
            return result_list
        else:
            raise ValueError("Input is not a valid list string.")
    except Exception as e:
        print("Error:", e)
        return ([])

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAuthorOrReadOnly])
def calculate_report_voip(request , number):
    
    Data=request.data
    idNumber = number 
    report_get=get_object_or_404(Report,id=idNumber)   
    getReport =  ReportSerializer(report_get)   



    result=Call_log_report(Data['start'],
                           Data['end'],
                           getReport.data['type'],
                           getReport.data['agent'],
                           getReport.data['queue_log'],
                           getReport.data['company']
                           )
   

    
    if  type(result)!=str:  
        voip_report= json.loads(result.to_json(orient='records'))
    
        return Response({
            "status" : True,
            "message" : "done" ,
            "data" : voip_report
        },status=200)
    else:
        return Response({
            "status" : False,
            "message" : "NO Report" ,
            "data" :  "NO Report"
        },status=400)


@permission_classes([IsAuthenticated,IsAuthorOrReadOnly])
class DeleteDetailAPIView(APIView):
    def get(self, request, report_id):
        report = get_object_or_404(Report, id=report_id)
        report_serializer = ReportSerializer(instance=report)
        data = report_serializer.data
        return Response({'report': data})

    def delete(self, request, report_id):
        report = get_object_or_404(Report, id=report_id)
        report.delete()
        return Response({'message': "deleted"})



@permission_classes([IsAuthenticated,])
@api_view(['POST'])
def report_update(request,report_id=None):
    Data=request.data
    User=request.user


    report = get_object_or_404(Report, id=report_id)
    report.name=Data['name']
    report.type=Data['type']
    report.agent=Data['agent']
    report.queue_log=Data['queue_log']
    report.company= Data['company']
    report.save()
    return Response({'message': "updated"})



        



@permission_classes([IsAuthenticated,])
@api_view(['POST'])
def report_create(request,report_id=None):
    Data=request.data
    User=request.user


    Report.objects.create(name=Data['name'],
                          type=Data['type'],
                          agent=Data['agent'],
                          queue_log=Data['queue_log'],
                          company=Data['company'],
                          author=User
    )
    return Response({'message': "created"},status=status.HTTP_201_CREATED)


    





@permission_classes([IsAuthenticated])
class ReportList(ListAPIView):
    queryset =Report.objects.all()
    serializer_class =ReportSerializer
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(author=user)
    



@api_view(['POST'])
@permission_classes([IsAuthorOrReadOnly, IsAuthenticated,])
def report_excell(request, number):
    Data = request.data
    idNumber = number 
    report_get = get_object_or_404(Report, id=idNumber)   
    getReport =  ReportSerializer(report_get)   




    result = Call_log_report_excell(Data['start'],
                             Data['end'],
                             getReport.data['type'],
                             getReport.data['agent'],
                             getReport.data['queue_log'],
                             getReport.data['company']
                             )

    if isinstance(result, str):
        return HttpResponse(result, content_type="text/plain")
    else:
        excel_buffer = BytesIO()


        with pd.ExcelWriter(excel_buffer,mode="w") as writer:
            result.to_excel(writer, sheet_name="1", index=False)

        excel_buffer.seek(0)
        excel_data = excel_buffer.getvalue()
        
        if len(excel_data) == 0:
            print("Excel data is empty")
        else:
            print("Excel data is not empty")


        
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
        
        return response



