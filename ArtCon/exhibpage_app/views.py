from django.shortcuts import render
from exhibpage_app.models import Performance, Location
# 페이지 로드
def exhibition(request):
    pk = request.GET.get('exhibitID')
    performance_data = list(Performance.objects.filter(id__exact=pk).values())
    print(performance_data)
    p_location = performance_data[0]['L_name'].split()[0]
    print(p_location)
    location = list(Location.objects.filter(L_name__startswith=p_location).values())
    print(location)
    print(performance_data[0])
    performance_data[0]['la'] = location[0]['L_la']
    performance_data[0]['lo'] = location[0]['L_lo']

    context = {'exhibit':performance_data}

    return render(request, "exhibpage_app/single.html", context=context)