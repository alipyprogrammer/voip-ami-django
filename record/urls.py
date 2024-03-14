from django.urls import path , include,re_path 
from . import views
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


urlpatterns = [
    path('erfanLog/' ,views.AddLogOnlineHamkadeh ,name="erfanLog"),
    path('voip-log/' ,views.AddVoipLogOnlineHamkadeh ,name="voip-log"),
    path('reservations/' ,views.AddReservationHamkadeh ,name="reservation"),


    path('log/status/consultant' ,views.LogStatusUserConsultantDetail ,name="LogStatusUserConsultantDetail"),
    path('reservation/consultant' ,views.DetailReservationsHamkadeh ,name="DetailReservationsHamkadeh"),
    path('voip/log/status/consultant' ,views.LogStatusVoipUserConsultantDetail ,name="LogStatusVoipUserConsultantDetail"),
    path('excel/voip-and-reservations' ,views.ExcelAmarVoipAndReservation ,name="ExcelAmarVoipAndReservation"),





]

