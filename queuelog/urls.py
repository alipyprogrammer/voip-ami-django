from django.urls import path , include,re_path 
from . import views
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('add-log/' ,views.AddQueueLog ,name="add_log_voip"),
    path('last-log/' ,views.LastQueueLog ,name="lastLog"),
]

