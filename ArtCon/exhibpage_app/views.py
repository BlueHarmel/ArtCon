from django.shortcuts import render
from exhibpage_app.models import Exhibit

# 페이지 로드
def exhibition_2(request):
    pk = request.GET.get('exhibitID')
    exhibit = Exhibit.objects.filter(id__exact=pk)
    context = {'exhibit':exhibit}
    return render(request, "exhibpage_app/single.html", context=context)