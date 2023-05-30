import json, pandas as pd
from artAddress import DB
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from sklearn.metrics.pairwise import linear_kernel
import re


def remove_special_characters(text):
    # 특수 문자와 한자를 제거하는 정규 표현식 패턴
    pattern = r"[^\w\s]|[\u4e00-\u9fff]+"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


stopwords = ["을", "를", "이", "가", "은", "는"]
okt = Okt()
tfidf_vectorizer = TfidfVectorizer(tokenizer=okt.morphs, stop_words=stopwords)

exhibition_names = []

for db in DB:
    # Read the JSON file
    with open(
        db,
        encoding="utf-8-sig",
    ) as file:
        data = json.load(file)
        exhibition_names.extend(
            [remove_special_characters(item["data1"]["전시회명"]) for item in data]
        )

# TF-IDF 행렬 생성
tfidf_matrix = tfidf_vectorizer.fit_transform(exhibition_names)
print(tfidf_matrix.shape)
# TF-IDF 행렬 확인
print(tfidf_matrix)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print(cosine_sim.shape)

indices = pd.Series(df2.index, index=df2["title"]).drop_duplicates()


def get_recommendations(title, cosine_sim=cosine_sim):
    # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
    idx = indices[title]
    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))
    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    sim_scores = sim_scores[1:11]
    # 추천 영화 목록 10개의 인덱스 정보 추출
    movie_indices = [i[0] for i in sim_scores]
    # 인덱스 정보를 통해 영화 제목 추출
    return df2["title"].iloc[movie_indices]
