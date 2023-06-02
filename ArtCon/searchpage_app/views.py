from django.shortcuts import render
from exhibpage_app.models import Exhibit
import datetime


def search(request):
    searched_title = request.POST.get("searched", "")
    searched_date = request.POST.get("date", "")

    if searched_title == "":
        if searched_date == "":
            return render(request, "searchpage_app/search.html")
        else:
            exhibits = list(
                Exhibit.objects.filter(
                    start_date__lte=searched_date, end_date__gte=searched_date
                ).values()
            )
            context = {"searched_date": searched_date, "exhibits": exhibits}
            return render(request, "searchpage_app/search.html", context=context)
    else:
        if searched_date == "":
            exhibits = Exhibit.objects.filter(E_name__contains=searched_title)
            return render(
                request,
                "searchpage_app/search.html",
                {"searched_title": searched_title, "exhibits": exhibits},
            )
        else:
            exhibits = list(
                Exhibit.objects.filter(
                    E_name__contains=searched_title,
                    start_date__lte=searched_date,
                    end_date__gte=searched_date,
                ).values()
            )
            context = {
                "searched_title": searched_title,
                "searched_date": searched_date,
                "exhibits": exhibits,
            }
            return render(request, "searchpage_app/search.html", context=context)
