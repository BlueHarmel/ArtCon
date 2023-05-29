from django.urls import path
from . import views


urlpatterns = [
    path("", views.exhibition_2, name="exhibition"),
]
