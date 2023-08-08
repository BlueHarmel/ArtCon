from django.shortcuts import render
from exhibpage_app.models import Performance, Location
# 페이지 로드
def exhibition(request):
    pk = request.GET.get('exhibitID')
    exhibit = list(Performance.objects.filter(id__exact=pk).values())
    res_exhibit = []
    location = list(Location.objects.filter(L_name__exact=exhibit[0]['L_name']).values())
    exhibit[0]['x'] = location[0]['x']
    exhibit[0]['y'] = location[0]['y']

    context = {'exhibit':exhibit}

    return render(request, "exhibpage_app/single.html", context=context)