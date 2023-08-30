from django.shortcuts import render, redirect
from exhibpage_app.models import Performance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict
import json
import time
from authpage_app.models import User

def search(request):
    print(request.GET)
    user_id = request.user.username
    searched_name = request.GET.get("name", "")
    searched_date = request.GET.get("date", "")
    searched_genre = request.GET.get("genre", "")
    context = {}
    exhibits = Performance.objects.all()

    # log dict
    if user_id:
        user_data = User.objects.filter(username__exact=user_id)
        user_age = user_data[0]['age']
        user_gender = user_data[0]['gender']
    else:
        user_age = ''
        user_gender = ''
    log_text = {'user_id': user_id, 'user_age': user_age, 'user_gender': user_gender, 'page': 'searchpage', 'searched_name': searched_name, 'searched_date': searched_date, 'searched_genre': searched_genre}
    

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

        if int(page) == 1:
            query_params = QueryDict(mutable=True)
            query_params["page"] = 1
            if searched_name:
                query_params["name"] = searched_name
            if searched_date:
                query_params["date"] = searched_date
            if searched_genre:
                query_params["genre"] = searched_genre
            if (
                query_params.urlencode() != request.GET.urlencode()
            ):  # 검색 조건이 변경되었을 때만 리다이렉트 수행
                return redirect(request.path_info + "?" + query_params.urlencode())
    logging(log_text)

    return render(request, "searchpage_app/search.html", context=context)

def logging(log_dict):
    with open('../test.log', 'a', encoding='utf-8') as f:
        text = json.dumps(log_dict) + '\n'
        f.write(text)