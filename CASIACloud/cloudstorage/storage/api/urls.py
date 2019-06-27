from django.urls import path
from . import views

app_name = 'storage'

urlpatterns = [
    path('device/', views.deviceListView.as_view(), name='device_list'),
]