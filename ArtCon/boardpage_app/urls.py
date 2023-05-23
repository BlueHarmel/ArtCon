from django.urls import path
from . import views


urlpatterns = [
    path("", views.board, name="board"),
    path("write/", views.write, name="write"),
]
