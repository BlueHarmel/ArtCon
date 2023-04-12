from django.urls import path
from . import views

# url패턴에서 'mainpage_app/'이 항상 먼저 나옴
urlpatterns = [
    path("search/", views.search_view),
    path("map/", views.map_view),
]  # /mainpage_app --> Project urls.py
