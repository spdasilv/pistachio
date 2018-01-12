from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('viewAjax/', views.viewAjax.as_view(), name='viewAjax'),
    path('selectCity/', views.selectCityView.as_view(), name='selectCity'),
    path('<int:pk>/createTrip/', views.createTripView.as_view(), name='createTrip'),
    path('requestAjax/', views.requestAjax, name='requestAjax'),
]