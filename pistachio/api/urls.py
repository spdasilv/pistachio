from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'api'
urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.homeView.as_view(), name='home'),
    path('newTrip/', views.newTrip, name='newTrip'),
    path('bidLocations/', views.bidLocationView.as_view(), name='bidLocations'),
    path('adminGA/', views.adminGAView.as_view(), name='adminGA'),
    path('<int:pk>/drag_drop/', views.dragDropView.as_view(), name='drag_drop'),
    path('<int:pk>/selectActivities/', views.selectActivitiesView.as_view(), name='selectActivities'),
    path('bidAjax/', views.bidAjax, name='bidAjax'),
    path('addActivitiesAjax/', views.addActivitiesAjax, name='addActivitiesAjax'),
    path('runGA/', views.runGA, name='runGA'),
]