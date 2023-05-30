from django.shortcuts import render
from exhibpage_app.models import Exhibit
import datetime


# Create your views here.
def date_search(request):
    date = request.GET.get("date")
    searched = list(
        Exhibit.objects.filter(
            start_date__lte=datetime.date(2023, 5, 29),
            end_date__gte=datetime.date(2023, 6, 30),
        ).values()
    )
    # for i in range(len(searched)):
    # context[i] = searched[0]
    context = {"searched": searched}
    return render(request, "searchpage_app/search.html", context=context)
