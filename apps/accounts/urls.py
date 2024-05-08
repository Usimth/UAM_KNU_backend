from django.urls import path
from .views import *

urlpatterns = [
    path("/register", RegisterView.as_view(), name='user_register'),
    path("/auth", AuthView.as_view(), name='user_auth'),
]
