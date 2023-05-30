from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from sklearn.metrics.pairwise import linear_kernel
import re
from exhibpage_app.models import Exhibit
from authpage_app.models import User

stopwords = ["을", "를", "이", "가", "은", "는"]
okt = Okt()
tfidf_vectorizer = TfidfVectorizer(tokenizer=okt.morphs, stop_words=stopwords)

exhibition_names = []


# Create your views here.
def recommend(request):
    get_recommendations()
    return render(request, "recompage_app/recommend.html")


def remove_special_characters(text):
    # 특수 문자와 한자를 제거하는 정규 표현식 패턴
    pattern = r"[^\w\s]|[\u4e00-\u9fff]+"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def get_recommendations(title):
    exhibits = Exhibit.objects.all()
    exhibits[0].pk
    df = pd.DataFrame(
        exhibits,
        columns=[
            "pk",
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
    indices = pd.Series(df["pk"], index=df["E_name"]).drop_duplicates()

    # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
    idx = indices[title]

    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    sim_scores = sim_scores[1:11]

    # 추천 영화 목록 10개의 인덱스 정보 추출
    exhibit_indices = [i[0] for i in sim_scores]

    # 인덱스 정보를 통해 영화 제목 추출
    return df["E_name"].iloc[exhibit_indices]
