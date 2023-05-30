from django.shortcuts import render
from exhibpage_app.models import Exhibit
import datetime

# Create your views here.
def search_date(request):
    searched_date = request.POST.get('date')
    exhibits_date = list(Exhibit.objects.filter(start_date__lte=datetime.date(2023,5,31),
                                        end_date__gte=datetime.date(2023,5,31)).values())
    context={'searched_date':searched_date, "exhibits": exhibits_date}
    return render(request, "searchpage_app/search.html", context=context)