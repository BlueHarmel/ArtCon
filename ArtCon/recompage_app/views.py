from django.shortcuts import render, redirect
from django.urls import reverse
import pandas as pd
from django.core import serializers
from sklearn.feature_extraction.text import TfidfVectorizer
# from konlpy.tag import Okt
# from konlpy.tag import Okt
from sklearn.metrics.pairwise import linear_kernel
import re
import pprint
from exhibpage_app.models import Performance
from authpage_app.models import User
from exhibpage_app.models import Location
from django.http import JsonResponse
from django.contrib import messages
from . import recommend_test
from datetime import datetime

# stopwords = ["을", "를", "이", "가", "은", "는"]
# okt = Okt()
# tfidf_vectorizer = TfidfVectorizer(tokenizer=okt.morphs, stop_words=stopwords)

# exhibition_names = []


# def recommend(request):
#     pass
# Create your views here.
# 2023 10대: 2014~2004, 20대: 2003~1993, 30대: 1992~1982, 40대: 1981~1971
def get_age_pfcode(user_id):
    gender_age = {
    'man_10_1': 'PF198878', 'man_10_2': 'PF189859',
    'man_20_1': 'PF192964', 'man_20_2': 'PF192978',
    'man_30_1': 'PF194963', 'man_30_2': 'PF145857',
    'man_40_1': 'PF194963', 'man_40_2': 'PF195242',
    'woman_10_1': 'PF196584', 'woman_10_2': 'PF198891',
    'woman_20_1': 'PF192964', 'woman_20_2': 'PF191916',
    'woman_30_1': 'PF138393', 'woman_30_2': 'PF145857',
    'woman_40_1': 'PF194963', 'woman_40_2': 'PF195242'
    }
    user_data = list(User.objects.filter(username__exact=user_id).values())[0]
    user_birth = datetime.strptime(str(user_data['birth']), '%Y-%m-%d')
    print(user_birth)
    today = datetime.now()
    age_10 = datetime.strptime('2014-01-01','%Y-%m-%d')
    age_20 = datetime.strptime('2003-01-01','%Y-%m-%d')
    age_30 = datetime.strptime('1982-01-01','%Y-%m-%d')
    age_40 = datetime.strptime('1971-01-01','%Y-%m-%d')
    if user_data['gender'] == 1:
        if user_birth < age_20:
            return list(gender_age['man_10_1'], gender_age['man_10_2'])
        elif age_20 <= user_birth and user_birth < age_30:
            return list(gender_age['man_20_1'], gender_age['man_20_2'])
        elif age_30 <= user_birth and user_birth < age_40:
            return list(gender_age['man_30_1'], gender_age['man_30_2'])
        else:
            return [gender_age['man_40_1'], gender_age['man_40_2']]
    else:
        if user_birth < age_20:
            return list(gender_age['woman_10_1'], gender_age['woman_10_2'])
        elif age_20 <= user_birth and user_birth < age_30:
            return list(gender_age['woman_20_1'], gender_age['woman_20_2'])
        elif age_30 <= user_birth and user_birth < age_40:
            return list(gender_age['woman_30_1'], gender_age['woman_30_2'])
        else:
            return list(gender_age['woman_40_1'], gender_age['woman_40_2'])
    # print(type(user_birth))
    # print(user_birth)
    # print(user_data)
    

def recommend(request):
    if request.user.is_anonymous:
        messages.warning(request, "로그인 후 이용가능합니다")
        url = reverse("authpage_app:login")
        return redirect(url)
    if request.method == "GET":
        user_id = request.user.username
        user_gender_age = get_age_pfcode(user_id)
        print(10)
        pfcodes = recommend_test.get_recommend(user_gender_age)
        print(20)
        exhibits = list(Performance.objects.filter(P_id__in=pfcodes).values())
        context = {"exhibits": exhibits}
        pprint.pprint(exhibits)
        return render(request, "recompage_app/recommend.html", context=context)
# def recommend(request):
#     return render(request, "recompage_app/recommend.html")


# Create your views here.
# def recommend(request):
#    if request.user.is_anonymous:
#        messages.warning(request, "로그인 후 이용가능합니다")
#        url = reverse("authpage_app:login")
#        return redirect(url)
#    if request.method == "GET":
#        rec_id = get_recommendations(request)
#        exhibits = list(Performance.objects.filter(id__in=rec_id).values())
#        context = {"exhibits": exhibits}
#        return render(request, "recompage_app/recommend.html", context=context)


    if request.method == "POST":
        latLng = request.body.decode("utf-8")
        s = latLng.split("&")[0][2:]
        w = latLng.split("&")[1][2:]
        n = latLng.split("&")[2][2:]
        e = latLng.split("&")[3][2:]
        # print('****swne****')
        # print(s,w,n,e)
        location = list(
            Location.objects.filter(x__gte=s, x__lte=n, y__gte=w, y__lte=e).values()
        )
        map_exhibits = []
        # print('****location****')
        # print(location)
        for i in location:
            l_name = i["L_name"]
            exhibit = list(Performance.objects.filter(L_name__exact=l_name).values())
            map_exhibit = {}
            map_exhibit["id"] = exhibit[0]["id"]
            map_exhibit["E_name"] = exhibit[0]["E_name"]
            map_exhibit["x"] = i["x"]
            map_exhibit["y"] = i["y"]
            # print("==============")
            # print(exhibit)
            map_exhibits.append(map_exhibit)
        context = {"map_exhibits": map_exhibits}
        # print("************")
        # print(context)
        return JsonResponse(context)


# def remove_special_characters(text):
#    # 특수 문자와 한자를 제거하는 정규 표현식 패턴
#    pattern = r"[^\w\s]|[\u4e00-\u9fff]+"
#    cleaned_text = re.sub(pattern, "", text)
#    return cleaned_text
#
#
# def get_recommendations(request):
#    user_name = request.user
#    user = User.objects.filter(username=user_name).values()
#    user = user[0]
#    exhibits = list(Performance.objects.all().values())
#    print(exhibits)
#    df = pd.DataFrame(
#        exhibits,
#        columns=[
#            "id",
#            "P_name",
#            "L_name",
#            "P_startdate",
#            "P_enddate",
#            "P_img",
#            "summary",
#        ],
#    )
#    # TF-IDF 행렬 생성
#    tfidf_matrix = tfidf_vectorizer.fit_transform(df["P_name"])
#    # TF-IDF 행렬 확인
#    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
#    indices = pd.Series(df.index, index=df["P_name"]).drop_duplicates()
#    # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
#    idx = indices[user["prefer_title"]]
#    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
#    sim_scores = list(enumerate(cosine_sim[idx]))
#    # 코사인 유사도 기준으로 내림차순 정렬
#    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
#    sim_scores = sim_scores[1:4]
#    # 추천 영화 목록 10개의 인덱스 정보 추출
#    exhibit_indices = [i[0] for i in sim_scores]
#    # print(df["id"].iloc[exhibit_indices])
#    rec_id = df["id"].iloc[exhibit_indices].tolist()
#    # 인덱스 정보를 통해 영화 제목 추출
#    return rec_id
#
