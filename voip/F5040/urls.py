from django.urls import path
from .views import *
from . import views
from .views import *



urlpatterns = [
    path('peers/', views.PeersViews, name='peers'),
    path('queue/', views.QueueViews, name='queue'),
    path('active-channels/', views.ActiveChannels5040Views, name='active-channels'),
    path('line-list' , Member5040ListView.as_view()),




]
