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

urlpatterns = [
    # path('chat/', include('chat.urls')),
    path('', include('voip.urls')),
    path('5040/', include('voip.F5040.urls')),
    path('fellows/', include('voip.Hamkadeh_fellows.urls')),
    path('admin/', admin.site.urls),
    # path('api/users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/', include('User.urls')),
    path('api/record/', include('record.urls')),
    path('api/queuelog/', include('queuelog.urls')),
]

urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
