from django.shortcuts import render
from django.http import HttpResponse


articles = {"search": "Search Page", "map": "Map Page"}


# Create your views here.
def search_view(request):
    return HttpResponse(articles["search"])


def map_view(request):
    return HttpResponse(articles["map"])
