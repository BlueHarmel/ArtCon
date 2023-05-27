from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
import json
from exhibpage_app.models import Exhibit
from django.core import serializers

# Create your views here.
# 메인페이지인데 변수 이름을 recommend라 했는데 수정 필요할지도
def mainpage_app(request):
    recommend1 = serializers.serialize('json', Exhibit.objects.filter(E_name__contains='꼴값쇼:'))
    recommend2 = serializers.serialize('json', Exhibit.objects.filter(E_name__contains='파랑새를'))
    recommend3 = serializers.serialize('json', Exhibit.objects.filter(E_name__contains='전통공예명품전'))
    recommend4 = serializers.serialize('json', Exhibit.objects.filter(E_name__contains='달마가'))
    banner1 = serializers.serialize('json', Exhibit.objects.filter(E_name__contains='바당수업'))
    banner2 = serializers.serialize('json', Exhibit.objects.filter(E_name__contains='나전장의'))
    banner3 = serializers.serialize('json', Exhibit.objects.filter(E_name__contains='오프그리드'))
    context = {"recommend1":recommend1, "recommend2":recommend2, "recommend3":recommend3, "recommend4":recommend4,
               "banner1":banner1, "banner2":banner2, "banner3":banner3}
    return render(request, "mainpage_app/index.html", context=context)