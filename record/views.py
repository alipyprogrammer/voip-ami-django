from rest_framework import generics
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import *
import colorama
from django.views import View
from colorama import Fore
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime , timedelta
import json
import requests
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
from .serializers import ReservationsHamkadehSerializer
from User.permissions import *
from time import sleep
import openpyxl
import pandas as pd
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def AddReservationHamkadeh(request):
    Data = request.data
    User = request.user
    log_entries = []
    
    if User.robotHamkadeh :
        file_name="Reservation.json"
        loaded_dict = None
        with open(file_name, 'r', encoding='utf-8') as file:
            loaded_dict = json.load(file)
        log_entry = []
        log_create = []
        for i in Data['data']:

            if loaded_dict == [{}] :
                result_dict = None            
            else:
                filtered_dicts = (dictionary for dictionary in loaded_dict if dictionary.get("id") == i['id'])
                result_dict = next(filtered_dicts, None)

            if result_dict is not None:
                if result_dict != i:
                    IsCheck = ReservationsHamkadeh.objects.using("hamkadeh").filter(idd=i['id'])
                    IsExsit = IsCheck.exists() 
                    IsFirst = IsCheck.first()
                    end_date  = datetime.strptime(i['reserve_timestamp'], "%Y-%m-%d %H:%M:%S")
                    end_date  = end_date  + timedelta(seconds=i['reserve_duration'])
                    consultantCheck = UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd=i['consultant_id']).first()
    
                    if IsExsit :
                        IsFirst.consultant_id = consultantCheck
                        IsFirst.client_id = i['client_id']
                        IsFirst.start_date = i['reserve_timestamp']
                        IsFirst.end_date = end_date
                        IsFirst.status = i['status']
                        IsFirst.created_at = i['created_at']
                        IsFirst.updated_at = i['updated_at']
                        IsFirst.save()
                    else:
                        create = ReservationsHamkadeh(
                            idd = i['id'],
                            consultant_id = consultantCheck,
                            client_id = i['client_id'],
                            start_date = i['reserve_timestamp'],
                            end_date = end_date,
                            status = i['status'],
                            created_at = i['created_at'],
                            updated_at = i['updated_at'],
                        )
                        log_create.append(create)
            else :
                end_date  = datetime.strptime(i['reserve_timestamp'], "%Y-%m-%d %H:%M:%S")
                end_date  = end_date  + timedelta(seconds=i['reserve_duration'])

                IsCheck = ReservationsHamkadeh.objects.using("hamkadeh").filter(idd=i['id'])
                IsExsit = IsCheck.exists() 
                IsFirst = IsCheck.first() 
                consultantCheck = UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd=i['consultant_id']).first()

                if IsExsit :
                    IsFirst.consultant_id = consultantCheck
                    IsFirst.client_id = i['client_id']
                    IsFirst.start_date = i['reserve_timestamp']
                    IsFirst.end_date = end_date
                    IsFirst.status = i['status']
                    IsFirst.created_at = i['created_at']
                    IsFirst.updated_at = i['updated_at']
                    IsFirst.save()
                else:

                    create = ReservationsHamkadeh(
                        idd = i['id'],
                        consultant_id = consultantCheck,
                        client_id = i['client_id'],
                        start_date = i['reserve_timestamp'],
                        end_date = end_date,
                        status = i['status'],
                        created_at = i['created_at'],
                        updated_at = i['updated_at'],
                    )
                    log_create.append(create)
        ReservationsHamkadeh.objects.using("hamkadeh").bulk_create(log_create)
        file_name="Reservation.json"
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(Data['data'], file, ensure_ascii=False, indent=4)

        return Response({
             "status": True,
             "message": "done",
             "data": None
         }, status=200)
    else :
        return Response({
             "status": False,
             "message": "failed",
             "data": None
         }, status=403)



@api_view(['POST'])
def AddLogOnlineHamkadeh(request):
    Data = request.data
    User = request.user
    log_entries = []
    file_name="ErfanLogOnline.json"
    loaded_dict = None
  
  
    if User.robotHamkadeh :
  
  
        with open(file_name, 'r', encoding='utf-8') as file:
            loaded_dict = json.load(file)
        log_entry = []
        for i in Data['data']:

            if loaded_dict == [{}] :
                result_dict = None            
            else:
                filtered_dicts = (dictionary for dictionary in loaded_dict if dictionary.get("id") == i['id'])
                result_dict = next(filtered_dicts, None)

            if result_dict is None:
                IsRecord = LogOnlineHamkadeh.objects.using("hamkadeh").filter(idd=i['id']).exists()
                if not IsRecord:
                    ####################################
                    # consultant
                    if i['consultant_id'] is not None:
                        consultantCheck = UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd=i['consultant_id']).first()
                    else:
                        consultantCheck = None
                    ####################################

                    ####################################
                    # support
                    if i['support_id'] is not None:
                        supportCheck = UsersHamkadeh.objects.using("hamkadeh").filter(support_idd=i['support_id']).first()
                    else:
                        supportCheck = None
                    ####################################

                    log_entry = LogOnlineHamkadeh(
                        idd=i['id'],
                        consultant_idd=consultantCheck,
                        support_idd=supportCheck,
                        status=i['status'],
                        date=i['created_at'],
                    )
                    log_entries.append(log_entry)
        if log_entry  is not []: 
            LogOnlineHamkadeh.objects.using("hamkadeh").bulk_create(log_entries)

        file_name="ErfanLogOnline.json"
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(Data['data'], file, ensure_ascii=False, indent=4)


        return Response({
            "status": True,
            "message": "done",
            "data": None
        }, status=200)
    else:
        return Response({
            "status": False,
            "message": "failed",
            "data": None
        }, status=403)






@api_view(['POST'])
def AddVoipLogOnlineHamkadeh(request):
    Data = request.data['data']

    file_name="VoipLogOnline.json"
    loaded_dict = None
    with open(file_name, 'r', encoding='utf-8') as file:
        loaded_dict = json.load(file)

    addLog = []

    for i in Data:
        
        getOperatorNumber =  i['name']

        find = getOperatorNumber.find("/")

        if find != "-1":
             getOperatorNumber = getOperatorNumber[:find]



        filtered_dicts = (dictionary for dictionary in loaded_dict if dictionary.get("name") == i['name'])
        result_dict = next(filtered_dicts, None)
        if result_dict is not None:
            if i['status'][0:2] != result_dict['status'][0:2]:
                if i['status'][0:2] == "UN":
                    getUser = UsersHamkadeh.objects.using("hamkadeh").filter(operator_number=getOperatorNumber)
                    getUserExists =getUser.exists() 
                    getUser = getUser.first()
                    if getUserExists:
                        create = VoipLogOnlineHamkadeh(
                            user =getUser ,
                            status = "0"
                        )
                        addLog.append(create)

                if i['status'][0:2] == "OK":
                    getUser = UsersHamkadeh.objects.using("hamkadeh").filter(operator_number=getOperatorNumber)
                    getUserExists =getUser.exists() 
                    getUser = getUser.first()

                    if getUserExists:
                        create = VoipLogOnlineHamkadeh(
                            user =getUser ,
                            status = "1"
                        )
                        addLog.append(create)
        else:
                if i['status'][0:2] == "UN":
                    getUser = UsersHamkadeh.objects.using("hamkadeh").filter(operator_number=getOperatorNumber)
                    getUserExists =getUser.exists() 
                    getUser = getUser.first()

                    if getUserExists:
                        create = VoipLogOnlineHamkadeh(
                            user =getUser ,
                            status = "0"
                        )
                        addLog.append(create)

                if i['status'][0:2] == "OK":
                    getUser = UsersHamkadeh.objects.using("hamkadeh").filter(operator_number=getOperatorNumber)
                   
                    getUserExists =getUser.exists() 
                    getUser = getUser.first()

                    if getUserExists:
                        create = VoipLogOnlineHamkadeh(
                            user =getUser ,
                            status = "1"
                        )
                        addLog.append(create)


    VoipLogOnlineHamkadeh.objects.using("hamkadeh").bulk_create(addLog)
    file_name="VoipLogOnline.json"
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(Data, file, ensure_ascii=False, indent=4)



    return Response({
        "status": True,
        "message": "done",
        "data": None
    }, status=200)














@api_view(['GET'])
def LogStatusUserConsultantDetail(request):
    
    
    User = request.user
    if User.statusConsultantHamkadeh:
        Id = request.GET.get('Id')
        Date = request.GET.get('Date')

        Date = datetime.strptime(Date, "%Y-%m-%d")
        Date      = Date.replace(hour=00 ,minute=00 , second=00)


        getAllUser  =  UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd = Id).first()
        getLog      =  LogOnlineHamkadeh.objects.using("hamkadeh").filter(
            consultant_idd__consultant_idd=Id,
            date__gte=Date
            ).values(
                "status" , "date"
            ).order_by("date")

        gabl = { "start" : None , "end" : None} 
        dic_log = []

        for i in getLog:

            if i['status'] == "1":
                gabl = {
                    "start" : i['date'],
                    "end"   : None
                }

            if i['status'] == "0" :
                if  gabl['start'] is not None:
                    gabl = {
                    "start" : gabl['start'] ,
                    "end"   : i['date']
                    }

            if gabl["start"] is not None and gabl["end"] is not None:
                dic_log.append({
                        "start" : gabl['start'].strftime("%Y-%m-%d %H:%M") ,
                        "end"   : gabl['end'].strftime("%Y-%m-%d %H:%M")
                })
                gabl = { "start" : None , "end" : None}



        return Response({
            "status": True,
            "message": "done",
            "count": len(dic_log),
            "data": dic_log
        }, status=200)

    else:

        return Response({
            "status": False,
            "message": "failed",
            "count": 0,
            "data": "403"
        }, status=403)


    

@api_view(['GET'])
def LogStatusVoipUserConsultantDetail(request):
    
    User = request.user
    if User.statusConsultantHamkadeh:
        Id = request.GET.get('Id')
        Date = request.GET.get('Date')

        Date = datetime.strptime(Date, "%Y-%m-%d")
        Date      = Date.replace(hour=00 ,minute=00 , second=00)


        getLog      =  VoipLogOnlineHamkadeh.objects.using("hamkadeh").filter(
            user__operator_number=Id,
            date__gte=Date
            ).values(
                "status" , "date"
            ).order_by("date")

        gabl = { "start" : None , "end" : None} 
        dic_log = []

        for i in getLog:

            if i['status'] == "1":
                gabl = {
                    "start" : i['date'],
                    "end"   : None
                }

            if i['status'] == "0" :
                if  gabl['start'] is not None:
                    gabl = {
                    "start" : gabl['start'] ,
                    "end"   : i['date']
                    }

            if gabl["start"] is not None and gabl["end"] is not None:
                dic_log.append({
                        "start" : gabl['start'].strftime("%Y-%m-%d %H:%M") ,
                        "end"   : gabl['end'].strftime("%Y-%m-%d %H:%M")
                })
                gabl = { "start" : None , "end" : None}



        return Response({
            "status": True,
            "message": "done",
            "count": len(dic_log),
            "data": dic_log
        }, status=200)

    else:

        return Response({
            "status": False,
            "message": "failed",
            "count": 0,
            "data": "403"
        }, status=403)



@api_view(['GET'])
def DetailReservationsHamkadeh(request):
    
    User = request.user
    if User.statusConsultantHamkadeh:
        Id = request.GET.get('Id')
        Date = request.GET.get('Date')

        Date = datetime.strptime(Date, "%Y-%m-%d")
        Date      = Date.replace(hour=00 ,minute=00 , second=00)

        getAllUser  =  UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd = Id).first()
        getLog      =  ReservationsHamkadeh.objects.using("hamkadeh").filter(
            consultant_id__consultant_idd=Id,
            start_date__gte=Date
            ).order_by(
                "start_date"
        ).exclude(status__in=["canceled" ,"pending"])

        getLogSerializers = ReservationsHamkadehSerializer(getLog ,many=True)

        return Response({
            "status": True,
            "message": "done",
            "count": len(getLog),
            "data": getLogSerializers.data
        }, status=200)

    else:

        return Response({
            "status": False,
            "message": "failed",
            "count": 0,
            "data": "403"
        }, status=403)
 


@api_view(['GET'])
def ExcelAmarVoipAndReservation(request):

    User = request.user
    if User.statusConsultantHamkadeh:
        Id = request.GET.get('Id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        getAllUser  =  UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd__isnull = False , status=1)

        # ReservationsHamkadeh
        ###########################################################################
        queries_consultant_resvvations_id = [Q(consultant_id__consultant_idd= i.consultant_idd ,start_date__gte=start_date ,start_date__lte=end_date , status__in=["reserved" ,"changed"] ) for i in getAllUser ]
        combined_query_consultant_reservations = queries_consultant_resvvations_id[0]
        for query in  queries_consultant_resvvations_id[1:]:
            combined_query_consultant_reservations |= query
        getReservationsHamkadeh =  ReservationsHamkadeh.objects.using("hamkadeh").filter(combined_query_consultant_reservations)
        print(len(getReservationsHamkadeh))
        ###########################################################################
        
        # Is User
        ###########################################################################
        IsUsergetReservationsHamkadeh = getReservationsHamkadeh.values_list("consultant_id__consultant_idd" , flat=True) 
        IsUsergetReservationsHamkadeh = list(set(IsUsergetReservationsHamkadeh))
        print(len(IsUsergetReservationsHamkadeh))
        ###########################################################################
        

        # LogVoip
        ###########################################################################
        queries_consultant_voip_id = [Q(user__consultant_idd= i ,date__gte=start_date ,date__lte=end_date ) for i in IsUsergetReservationsHamkadeh ]
        combined_query_consultant_voip = queries_consultant_voip_id[0]
        for query in  queries_consultant_voip_id[1:]:
            combined_query_consultant_voip |= query

        getVoipLogOnlineHamkadeh = VoipLogOnlineHamkadeh.objects.using("hamkadeh").filter(combined_query_consultant_voip)
        print(len(getVoipLogOnlineHamkadeh))
        ###########################################################################




        for userData in IsUsergetReservationsHamkadeh:
            print("omadam")
            filter_getReservationsHamkadeh =getReservationsHamkadeh.filter(consultant_id__consultant_idd=userData)
            print(len(filter_getReservationsHamkadeh))
            for timeData in filter_getReservationsHamkadeh:  
                print("injam kos kesh")
                filter_getVoipLogOnlineHamkadeh =  getVoipLogOnlineHamkadeh.filter(
                    user__consultant_idd=userData,
                    date__gte=timeData.start_date, 
                    date__lte=timeData.end_date, 
                )
                print(filter_getVoipLogOnlineHamkadeh)

        

        return Response({
            "status": True,
            "message": "success",
            "count": 0,
            "data": "an"
        }, status=200)



    else:

        return Response({
            "status": False,
            "message": "failed",
            "count": 0,
            "data": "403"
        }, status=403)
