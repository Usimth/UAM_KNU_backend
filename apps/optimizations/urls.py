from django.urls import path
from . import views

app_name = 'optimizations'

urlpatterns = [
    path('',views.optimizer().as_view(),name='optimizer')
]