from django.urls import path
from . import views

app_name = 'marketing_report'

urlpatterns = [
    path('', views.index, name='main'),
]