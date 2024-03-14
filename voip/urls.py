from django.urls import path
from .views import *
from . import views
from .views import *
urlpatterns = [
    path('active-channels/', views.ActiveChannelsViews, name='active-channels'),
    
    path('listen-hamkadeh/', views.ListeningHamkadehView, name='ListeningHamkadehView'),
    path('listen-5040/', views.Listening5040, name='Listening5040'),
    path('listen-sale-hamkadeh/', views.ListeningSaleHamkadeh, name='Listening5040'),



    path('peer-to-line/', views.PeerToLine, name='PeerToLine'),
    path('peer-to-line-excel/', views.PeerToInExcelLine, name='PeerToInExcelLine'),
    
    
    path('peer-remove-line/hamkadeh/', views.PeerRemoveLine, name='PeerRemoveLine'),
    path('peer-remove-line/5040/', views.PeerRemoveLine5040, name='PeerRemoveLine5040'),
    path('peer-remove-line/sale-hamkadeh/', views.PeerRemoveLineSaleHamkadeh, name='PeerRemoveLineSaleHamkadeh'),







    path('peers/', views.PeersViews, name='peers'),
    
    path('queue/', views.QueueViews, name='queue'),

    # path('line-list' , views.ListLineViews),
    path('line-list' , MemberListView.as_view()),
    

    

    
    # path('test' , Test.as_view())
    
    
    
    path('forward-list' , ForwardListView.as_view()),
    path('forward-add' , views.ForwardView),

    path('forward-add-excel' , views.ForwardInExcelView),



    


]
