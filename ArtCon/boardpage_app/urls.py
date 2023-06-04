from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("", views.board, name="board"),
    path("write/", views.write, name="write"),
    path("<int:pk>/", views.board_single, name="board_single"),
    path("<int:pk>/delete/", views.board_delete, name="board_delete"),
    path("<int:pk>/modify/", views.board_modify, name="board_modify"),
]
