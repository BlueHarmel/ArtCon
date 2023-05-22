from django.urls import path
from . import views

# url패턴에서 'mainpage_app/'이 항상 먼저 나옴
urlpatterns = [
    path("", views.mainpage_app, name="mainPage")
]  # /mainpage_app --> Project urls.py
