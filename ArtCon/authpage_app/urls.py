from django.urls import path
from . import views


urlpatterns = [
    path("login", views.login),
    path("findP", views.findP),
    path("register", views.register),
]
