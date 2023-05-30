from django.urls import path
from . import views


urlpatterns = [
    path("", views.search_2, name="search"),
]
