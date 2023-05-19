from django.urls import path
from . import views


urlpatterns = [
    path("board", views.board),
    path("write", views.write),
]
