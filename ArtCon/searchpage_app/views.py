from django.shortcuts import render
from exhibpage_app.models import Performance
import datetime


def search(request):
    searched_name = request.POST.get("searched", "")
    searched_date = request.POST.get("date", "")
    searched_genre = request.POST.get("genre","")

    if searched_name == "":
        if searched_date == "":
            if searched_genre == "":
                return render(request, "searchpage_app/search.html")
            else:
                performance_data = genre(searched_genre)
                context = {"searched_genre": searched_genre, "performance_data": performance_data}
                return render(request, "searchpage_app/search.html", context=context)
        else:
            if searched_genre == "":
                performance_data = date(searched_date)
                context = {"searched_date": searched_date, "performance_data": performance_data}
                return render(request, "searchpage_app/search.html", context=context)
            else:
                performance_data = date_genre(searched_date,searched_genre)
                context = {"searched_date":searched_date, "searched_genre":searched_genre, "perfornamce_data":performance_data}
                return render(request, "searchpage_app/search.html", context=context) 
    else:
        if searched_date == "":
            if searched_genre == "":
                performance_data = name(searched_name)
                context = {"searched_name": searched_name, "performance_data": performance_data}
                return render(request, "searchpage_app/search.html", context=context)
            else:
                performance_data = name_genre(searched_name,searched_genre)
                context = {"searched_name": searched_name, "searched_genre": searched_genre, "performance_data": performance_data}
                return render(request, "searchpage_app/search.html", context=context)
        else:
            if searched_genre == "":
                performance_data = name_date(searched_name, searched_date)
                context = {"searched_name": searched_name, "searched_date": searched_date, "performance_data": performance_data}
                return render(request, "searchpage_app/search.html", context=context)
            else:
                performance_data = name_date_genre(searched_name, searched_date, searched_genre)
                context = {"searched_name": searched_name, "searched_date": searched_date, "searched_genre": searched_genre, "performance_data": performance_data}
                return render(request, "searchpage_app/search.html", context=context)

def name(name):
    performance_data = Performance.objects.filter(P_name__contains=name)
    return performance_data
def date(date):
    performance_data = list(
                Performance.objects.filter(
                    P_startdate__lte=date, P_enddate__gte=date
                ).values()
            )
    return performance_data
def name_date(name, date):
    performance_data = list(
                Performance.objects.filter(
                    P_name__contains=name,
                    P_startdate__lte=date,
                    P_enddate__gte=date,
                ).values()
            )
    return performance_data
def genre(genre):
    performance_data = Performance.objects.filter(P_genre__contains=genre)
    return performance_data
def name_genre(name, genre):
    performance_data = Performance.objects.filter(P_name__contains=name, P_genre__contains=genre)
    return performance_data
def date_genre(date, genre):
    performance_data = list(
                Performance.objects.filter(
                    P_startdate__lte=date,
                    P_enddate__gte=date,
                    P_genre__contains=genre,
                ).values()
            )
    return performance_data
def name_date_genre(name, date, genre):
    performance_data = list(
                Performance.objects.filter(
                    P_name__contains=name,
                    P_startdate__lte=date,
                    P_enddate__gte=date,
                    P_genre__contains=genre,
                ).values()
            )
    return performance_data