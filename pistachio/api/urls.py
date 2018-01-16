from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'api'
urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('newTrip/', views.newTrip, name='newTrip'),
    path('selectCity/', views.selectCityView.as_view(), name='selectCity'),
    path('<int:pk>/createTrip/', views.createTripView.as_view(), name='createTrip'),
    path('requestAjax/', views.requestAjax, name='requestAjax'),
]