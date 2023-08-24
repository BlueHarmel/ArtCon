from django.shortcuts import render
from exhibpage_app.models import Performance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(request):
    print(request.GET)
    searched_name = request.GET.get("name", "")
    searched_date = request.GET.get("date", "")
    searched_genre = request.GET.get("genre", "")
    context = {}

    exhibits = Performance.objects.all()

    if searched_name:
        exhibits = exhibits.filter(P_name__contains=searched_name)
        context["searched_name"] = searched_name
    if searched_date:
        exhibits = exhibits.filter(
            P_startdate__lte=searched_date, P_enddate__gte=searched_date
        )
        context["searched_date"] = searched_date
    if searched_genre:
        exhibits = exhibits.filter(P_genre__contains=searched_genre)
        context["searched_genre"] = searched_genre

    if not (searched_name or searched_date or searched_genre):
        context["exhibits"] = None
    else:
        exhibits = exhibits.order_by("-P_startdate")
        paginator = Paginator(exhibits, 8)
        page = request.GET.get("page", 1)

        try:
            exhibits_page = paginator.page(page)
        except PageNotAnInteger:
            exhibits_page = paginator.page(1)
        except EmptyPage:
            exhibits_page = paginator.page(paginator.num_pages)

        context["exhibits"] = exhibits_page

    return render(request, "searchpage_app/search.html", context=context)
