from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
import json
from exhibpage_app.models import Exhibit
from django.core import serializers
from django.contrib import auth

# Create your views here.
# 메인페이지인데 변수 이름을 recommend라 했는데 수정 필요할지도
def mainpage_app(request):
    recommend1 = Exhibit.objects.filter(id__exact=1).values()
    recommend2 = Exhibit.objects.filter(id__exact=2).values()
    recommend3 = Exhibit.objects.filter(id__exact=3).values()
    recommend4 = Exhibit.objects.filter(id__exact=4).values()
    banner1 = Exhibit.objects.filter(id__exact=5).values()
    banner2 = Exhibit.objects.filter(id__exact=6).values()
    banner3 = Exhibit.objects.filter(id__exact=7).values()
    context = {
        "recommend1": recommend1,
        "recommend2": recommend2,
        "recommend3": recommend3,
        "recommend4": recommend4,
        "banner1": banner1,
        "banner2": banner2,
        "banner3": banner3,
    }
    if request.method == 'GET':
        return render(request, "mainpage_app/index.html", context)
    if request.method == 'POST':
        auth.logout(request)
        return render(request, "mainpage_app/index.html", context)
    
