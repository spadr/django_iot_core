from django.contrib import admin
from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.make_user.signupfunc, name='signup'),
    path('login/', views.sign_user.loginfunc, name='login'),
    path('logout/', views.sign_user.logoutfunc, name='logout'),
    path('read/', views.view_page.readfunc, name='read'),
    path('graph/', views.view_page.graphfunc, name='graph'),
    path('complete/<token>/', views.make_user.completefunc, name='complete'),
    path('', views.view_page.memefunc, name='meme'),
    path('console/', views.manipulate_data.consolefunc, name='console'),
    path('profile/', views.manipulate_data.profilefunc, name='profile'),
    path('postdata/', views.create_data.browserpostfunc, name='browserpost'),
    path('api/set/', views.create_data.DeviceSetApi.as_view(), name='set'),
    path('api/data/', views.create_data.DataReceiveApi.as_view(), name='data'),
    path('api/data/output/', views.create_data.DataSendApi.as_view(), name='output'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

