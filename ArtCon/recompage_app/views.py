from django.shortcuts import render, redirect
from django.urls import reverse
import pandas as pd
from django.core import serializers
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from sklearn.metrics.pairwise import linear_kernel
import re
from exhibpage_app.models import Exhibit
from authpage_app.models import User
from exhibpage_app.models import Location
from django.http import JsonResponse
from django.contrib import messages

stopwords = ["을", "를", "이", "가", "은", "는"]
okt = Okt()
tfidf_vectorizer = TfidfVectorizer(tokenizer=okt.morphs, stop_words=stopwords)

exhibition_names = []


# Create your views here.
def recommend(request):
    if request.user.is_anonymous:
        messages.warning(request, "로그인 후 이용가능합니다")
        url = reverse("authpage_app:login")
        return redirect(url)
    if request.method == "GET":
        rec_id = get_recommendations(request)
        exhibits = list(Exhibit.objects.filter(id__in=rec_id).values())
        context = {"exhibits": exhibits}
        return render(request, "recompage_app/recommend.html", context=context)

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
            exhibit = list(Exhibit.objects.filter(L_name__exact=l_name).values())
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


def remove_special_characters(text):
    # 특수 문자와 한자를 제거하는 정규 표현식 패턴
    pattern = r"[^\w\s]|[\u4e00-\u9fff]+"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def get_recommendations(request):
    user_name = request.user
    user = User.objects.filter(username=user_name).values()
    user = user[0]

    exhibits = list(Exhibit.objects.all().values())
    df = pd.DataFrame(
        exhibits,
        columns=[
            "id",
            "E_name",
            "L_name",
            "start_date",
            "end_date",
            "time",
            "fee",
            "url",
            "img",
            "summary",
        ],
    )
    # TF-IDF 행렬 생성
    tfidf_matrix = tfidf_vectorizer.fit_transform(df["E_name"])
    # TF-IDF 행렬 확인
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df["E_name"]).drop_duplicates()

    # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
    idx = indices[user["prefer_title"]]

    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    sim_scores = sim_scores[1:4]

    # 추천 영화 목록 10개의 인덱스 정보 추출
    exhibit_indices = [i[0] for i in sim_scores]
    # print(df["id"].iloc[exhibit_indices])
    rec_id = df["id"].iloc[exhibit_indices].tolist()
    # 인덱스 정보를 통해 영화 제목 추출
    return rec_id
