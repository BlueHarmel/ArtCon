from django.http.response import HttpResponse
from django.shortcuts import render
from exhibpage_app.models import Exhibit


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        exhibits = Exhibit.objects.filter(E_name__contains=searched)
        return render(
            request,
            "searchpage_app/search.html",
            {"searched": searched, "exhibits": exhibits},
        )
    else:
        return render(request, "searchpage_app/search.html", {})
