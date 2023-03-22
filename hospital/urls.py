from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('signIn', views.signIn),
    path('signUp', views.signUp),
    path('signOut', views.signOut),
]
