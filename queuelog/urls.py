from django.urls import path , include,re_path 
from . import views
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('add-log/' ,views.AddQueueLog_5040 ,name="add_log_voip"),
    path('last-log/' ,views.LastQueueLog_5040 ,name="lastLog"),
    path('add-log-hamkadeh/' ,views.AddQueueLog_hamkadeh ,name="add_log_voip"),
    path('last-log-hamkadeh/' ,views.LastQueueLog_hamkadeh ,name="lastLog"),
]






