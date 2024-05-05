from django.urls import path
from . import views

app_name = 'optimization'

urlpatterns = [
    path('',views.optimizer().as_view(),name='optimizer')
]