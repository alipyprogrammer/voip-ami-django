from django.urls import path , include,re_path 
from . import views
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfile,name="UserProfile"),
    path('list/' , UserList.as_view() , name='UserList'),
    # path('expert/list/' , ExpertList.as_view() , name='ExpertList'),
    # path('presenter/list/' , PresenterList.as_view() , name='PresenterList'),
  
  
    path('update/<str:pk>/' ,UserUpdate.as_view() ,name="UserUpdate"),
    path('delete/<str:pk>/' ,UserDelete.as_view() ,name="UserUpdate"),
    path('add/' ,views.UserAdd ,name="UserAdd"),
    # path('add/factor/' ,views.UserAddInFactor ,name="UserAddInFactor"),


    re_path(r'detail/(?P<id>[-\w]+)',UserDetail.as_view(),name ="ImageBlogDetailPanelAdmin"),




    path('record/user/add/' ,views.AddUserHamkadeh ,name="AddUserHamkadeh"),
    path('status/support' ,views.StatusUserSupportHamkadeh ,name="StatusUserSupportHamkadeh"),
    


    path('status/consultant' ,views.StatusUserConsultantHamkadeh ,name="StatusUserConsultantHamkadeh"),



]

