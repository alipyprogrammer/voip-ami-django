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
from . import call_log
from . call_log import *

urlpatterns = [
    
    path('call_log/<int:number>', calculate_report_voip),
    path('del-detail/<int:report_id>', DeleteDetailAPIView.as_view()),
    path('update/<int:report_id>', report_update),
    path('create', report_create),
    path('ReportList', ReportList.as_view()),
    path('excell/<int:number>', report_excell),
]





