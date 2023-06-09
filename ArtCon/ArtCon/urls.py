"""
URL configuration for ArtCon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mainpage_app.urls")),
    path("auth/", include("authpage_app.urls")),
    path("board/", include("boardpage_app.urls")),
    path("exhibition/", include("exhibpage_app.urls")),
    path("recommend/", include("recompage_app.urls")),
    path("search/", include("searchpage_app.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("logout/", LogoutView.as_view(next_page="mainPage"), name="logout"),
]
