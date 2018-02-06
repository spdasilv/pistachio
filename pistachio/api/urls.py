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
    path('', views.homeView.as_view(), name='home'),
    path('bidLocations/', views.bidLocationView.as_view(), name='bidLocations'),
    path('adminGA/', views.adminGAView.as_view(), name='adminGA'),
    path('drag_drop/', views.dragDropView.as_view(), name='drag_drop'),
    path('<int:pk>/createTrip/', views.createTripView.as_view(), name='createTrip'),
    path('requestAjax/', views.requestAjax, name='requestAjax'),
    path('getTrips/', views.requestAjax, name='getTrips'),
    path('bidAjax/', views.bidAjax, name='bidAjax'),
    path('runGA/', views.runGA, name='runGA'),
]