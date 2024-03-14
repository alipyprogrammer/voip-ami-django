from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework.decorators import  api_view,permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,RetrieveAPIView ,RetrieveUpdateAPIView,CreateAPIView,DestroyAPIView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from User import get_user_model
from User.models import *
from .permissions import * 
from .filter import *
from record.models import *
from django.db.models import Q
from functools import partial
from django.utils import timezone 
from datetime import datetime
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)



        serializers = UserSerializerWithToken(self.user).data
        for k , v in serializers.items():
            data[k]= v
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['message'] = 'سلام به سایت یقه خوش آمدید'
    
            # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user 
    serializer = UserSerializer(user , many=False)
    return Response(serializer.data)




class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes =(IsManager,)
    ordering ='-id'




# class ExpertList(ListAPIView):
#     queryset = User.objects.filter(Expert = True)
#     serializer_class= ExpertSerializer
#     permission_classes =(IsAdsManager,)
#     # filterset_class = UserFilter
#     ordering ='-id'


# class PresenterList(ListAPIView):
#     queryset = User.objects.filter(Presenter = True)
#     serializer_class= PresenterSerializer
#     permission_classes =(IsMonitoring,)
#     ordering ='-id'
  

class UserDetail(RetrieveAPIView):
    queryset =User.objects.all() 
    serializer_class =UserSerializer
    lookup_field ="id"
    permission_classes =(IsManager,)



# class UserAdd(CreateAPIView):
#     queryset =User.objects.all()
#     serializer_class =UserSerializer


@api_view(['PUT'])
@permission_classes([IsManager])
def UpdatePasswordUser(request): 
    user = request.user 
    serializer = UserSerializerWithToken(user , many=False)
    data = request.data 
    user.username   =  data['username']
    user.phoneNumber      =  data['phoneNumber']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)







# @api_view(['POST'])
# def UserAddInFactor(request):
#     data =request.data 
#     try :
#         users =get_user_model()
#         userCrate = users.objects.create( 
#             first_name =data['first_name'],
#             username   =data['username'],
#             phoneNumber=data['phoneNumber'],
#             Address=data['Address'],
#             HowSee=data['HowSee'],
#             HowSeePerson=data['HowSeePerson'],
#             birthday=data['birthday'],
#             IsCustomer=data['IsCustomer'],
#             password   =make_password(data['password']),
#         )
#         userGet=User.objects.get(phoneNumber=data['phoneNumber'])
#         StatusFactor = data['priceA']
#         serializer = UserSerializerWithToken(userCrate,many=False)
#         return Response(serializer.data)
#     except:
#         message = {'detail':'خطا '}
#         return Response(message, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
@permission_classes([IsManager])
def UserAdd(request):
    data =request.data 
    try :
        users =get_user_model()
        user = users.objects.create( 
            username   =data['username'],
            password   =make_password(data['password']),
        )
        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'خطا '}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(RetrieveUpdateAPIView):
    queryset =User.objects.all()
    serializer_class =UserSerializer


class UserDelete(DestroyAPIView):
    queryset =User.objects.all()
    serializer_class =UserSerializer



@api_view(['POST'])
def AddUserHamkadeh(request):
    Data = request.data
    user = request.user
    # if user.robotHamkadeh:
    
    if user.robotHamkadeh:
        for i in Data['data']:

            if i['consultant_id'] != None : 
                check  = UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd=i['consultant_id'])
            elif i['support_id'] != None :
                check  = UsersHamkadeh.objects.using("hamkadeh").filter(support_idd=i['support_id'])

            checkExit = check.exists()
            checkGet  = check.first()

            if checkExit:
                checkGet.consultant_idd     = i['consultant_id']
                checkGet.support_idd        = i['support_id']
                checkGet.operator_number    = i['operator_number']
                checkGet.name               = i['fullname']
                checkGet.profile            = i['profile']
                checkGet.status            = i['status']
                checkGet.save()
            else:  
                create = UsersHamkadeh.objects.using("hamkadeh").create(
                    consultant_idd   = i['consultant_id'],
                    support_idd      = i['support_id'],
                    operator_number  = i['operator_number'],
                    name             = i['fullname'],
                    profile          = i['profile'],
                )
        return Response({
            "status" : True,
            "message" : "done" ,
            "data" : None
        },status=201)
    else:
        return Response({
            "status" : False,
            "message" : "failed" ,
            "data" : None
        },status=403)



def filter_func_Consultant(item, remove):
    return item["consultant_idd"] != remove


@api_view(['GET'])
def StatusUserConsultantHamkadeh(request):
    Data = request.data
    user = request.user
    dic_list = []
    
    now      = timezone.now()
    now      = now.replace(hour=00 ,minute=00 , second=00)

    if user.statusConsultantHamkadeh:
        getAllUser  =  UsersHamkadeh.objects.using("hamkadeh").filter(consultant_idd__isnull = False)
        queries_consultant_id = [Q(consultant_idd__consultant_idd= i.consultant_idd , date__gte=now) for i in getAllUser if i.consultant_idd is not None]
        combined_query_consultant = queries_consultant_id[0]
        for query_consultant in queries_consultant_id[1:]:
            combined_query_consultant |= query_consultant
        getLog_consultant = LogOnlineHamkadeh.objects.using("hamkadeh").filter(combined_query_consultant).values("consultant_idd__consultant_idd" , "status" ,"date")
        LogID = []
        for i in getAllUser:
            filtered_consultants = [item for item in getLog_consultant if item.get('consultant_idd') == i.consultant_idd]
            if i.consultant_idd is not None:
                for log in getLog_consultant :
                    if int(log['consultant_idd__consultant_idd']) == int(i.consultant_idd):
                        partial_filter = partial(filter_func_Consultant, remove=i.consultant_idd)
                        filtered_list  = list(filter(partial_filter, LogID))
                        LogID            = filtered_list
                        LogID.append({
                            "consultant_idd" : i.consultant_idd, 
                            "name" :  i.name, 
                            "status" :  log['status'], 
                            "profile" :  i.profile, 
                            "operator_number" :  i.operator_number, 
                            "date" : log['date'].strftime("%Y-%m-%d %H:%M")
                        })
        return Response({
        "status": True,
        "message": "done",
        "count": len(LogID),
        "data": LogID
        }, status=200)
    else:
        return Response({
        "status": False,
        "message": "failed",
        "data": None
        }, status=403)



def filter_func_Support(item, remove):
    return item["support_idd"] != remove

@api_view(['GET'])
def StatusUserSupportHamkadeh(request):
    Data = request.data
    user = request.user
    dic_list = []
    now      = timezone.now()
    now      = now.replace(hour=00 ,minute=00 , second=00)
    
    if user.statusSupportHamkadeh:
        getAllUser  =  UsersHamkadeh.objects.using("hamkadeh").filter(support_idd__isnull = False)
        queries_consultant_id = [Q(support_idd__support_idd= i.support_idd ,date__gte=now ) for i in getAllUser ]
        combined_query_consultant = queries_consultant_id[0]
        for query_consultant in queries_consultant_id[1:]:
            combined_query_consultant |= query_consultant
        getLog_consultant = LogOnlineHamkadeh.objects.using("hamkadeh").filter(combined_query_consultant).values("support_idd__support_idd" , "status" , "idd" , "date")
        LogID = []
        for i in getAllUser:
            filtered_consultants = [item for item in getLog_consultant if item.get('support_idd') == i.support_idd]
            for log in getLog_consultant :
                    if int(log['support_idd__support_idd']) == int(i.support_idd):
                        partial_filter = partial(filter_func_Support, remove=i.support_idd)
                        filtered_list  = list(filter(partial_filter, LogID))
                        LogID            = filtered_list
                        LogID.append({
                            "support_idd" : i.support_idd, 
                            "name" :  i.name, 
                            "status" :  log['status'], 
                            "profile" :  i.profile, 
                            "operator_number" :  i.operator_number, 
                            "date" :  log['date'].strftime("%Y-%m-%d %H:%M") 

                        })
        return Response({
        "status": True,
        "message": "done",
        "count": len(LogID),
        "data": LogID
        }, status=200)
    else:
        return Response({
        "status": False,
        "message": "failed",
        "data": None
        }, status=403)
    
