from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login, name="login"),
    path("findP/", views.findP, name="findPassword"),
    path("register/", views.register, name="register"),
]
