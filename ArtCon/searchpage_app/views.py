from django.shortcuts import render
from exhibpage_app.models import Performance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(request):
    searched_title = request.GET.get("searched", "")
    searched_date = request.GET.get("date", "")
    context = {}

    exhibits = Performance.objects.all()

    if searched_title:
        exhibits = exhibits.filter(P_name__contains=searched_title)
        context["searched_title"] = searched_title
    if searched_date:
        exhibits = exhibits.filter(
            P_startdate__lte=searched_date, P_enddate__gte=searched_date
        )
        context["searched_date"] = searched_date
    exhibits = exhibits.order_by("-P_startdate")

    paginator = Paginator(exhibits, 8)  # 8 exhibits per page
    page = request.GET.get("page", 1)

    try:
        exhibits_page = paginator.page(page)
    except PageNotAnInteger:
        exhibits_page = paginator.page(1)
    except EmptyPage:
        exhibits_page = paginator.page(paginator.num_pages)

    context["exhibits"] = exhibits_page

    return render(request, "searchpage_app/search.html", context=context)
