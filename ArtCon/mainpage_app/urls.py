from django.urls import path
from . import views

# url패턴에서 'mainpage_app/'이 항상 먼저 나옴
urlpatterns = [path("", views.index, name="index")]  # /mainpage_app --> Project urls.py
