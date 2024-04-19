from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
from .views import *
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from . import Call_log
from . Call_log import *

urlpatterns = [
    
    path('call_log', ReportVoip),
]

