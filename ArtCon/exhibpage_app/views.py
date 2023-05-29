from django.shortcuts import render
<<<<<<< HEAD


# Create your views here.
def exhibition(request):
    return render(request, "exhibpage_app/single.html")
=======
from exhibpage_app.models import Exhibit

# 페이지 로드
def exhibition_2(request):
    pk = request.GET.get('exhibitID')
    exhibit = Exhibit.objects.filter(id__exact=pk)
    context = {'exhibit':exhibit}
    return render(request, "exhibpage_app/single.html", context=context)
>>>>>>> abb19d86dc7d37f02cf4a0523411bf0b9aa3a566
