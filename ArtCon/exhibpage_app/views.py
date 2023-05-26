from django.shortcuts import render
from exhibpage_app.models import Exhibit

# 페이지 로드
# single 페이지 로딩하면서 전시회명 넘겨줘야됨
def exhibition(request):
    data = Exhibit.objects.filter(E_name__startswith='에드워드')  
    return render(request, "exhibpage_app/single.html", context={'data':data})