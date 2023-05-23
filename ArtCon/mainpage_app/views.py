from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse


# Create your views here.
def mainpage_app(request):
    return render(request, "mainpage_app/index.html")
