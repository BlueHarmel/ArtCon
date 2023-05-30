from django.http.response import HttpResponse
from django.shortcuts import render
from exhibpage_app.models import Exhibit


def search(request):
    return render(request, "searchpage_app/search.html", {})

def search_title(request):
    if request.method == "POST":
        searched_title = request.POST["searched"]
        exhibits_title = Exhibit.objects.filter(E_name__contains=searched_title)
        return render(
            request,
            "searchpage_app/search.html",
            {"searched_title": searched_title, "exhibits": exhibits_title},
        )
