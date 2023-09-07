import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from scipy import sparse
import numpy as np
import datetime


def process_str(text):
    if isinstance(text, str):
        # 쉼표로 구분된 이름 추출 및 마지막에 있는 쉼표와 "등" 제거
        cast_names = [
            name.strip().lower().replace("등", "").replace(" ", "")
            for name in text.split(",")
            if name.strip()
        ]
        return cast_names
    elif isinstance(text, float) and np.isnan(text):
        return []  # NaN 데이터에 대해 빈 리스트 반환
    else:
        return []


def create_soup(x):
    return (
        " ".join(x["prfnm"])
        + " "
        + " ".join(x["prfcast"])
        + " "
        + " ".join(x["prfcrew"])
    )


def get_recommend(pfcode):
    pre_pf = pd.read_csv("C:/Users/home/Desktop/ArtCon/ArtCon/recompage_app/pre_pf.csv")
    print(1)
    # 'prfcast' 및 'prfcrew' 열의 데이터 처리
    for feature in ["prfnm", "prfcast", "prfcrew"]:
        pre_pf[feature] = pre_pf[feature].apply(process_str)
    print(2)
    pre_pf["soup"] = pre_pf.apply(create_soup, axis=1)
    tfidf_matrix = sparse.load_npz(
        "C:/Users/home/Desktop/ArtCon/ArtCon/recompage_app/test.npz"
    )
    print(3)
    # TF-IDF 행렬 확인
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(pre_pf["soup"], index=pre_pf.index).drop_duplicates()
    print(4)
    ##### test_data 아무거나 넣었을 때 작동하는지 확인
    ##### 변수: pfcode
    test_data = pre_pf.loc[pre_pf["mt20id"] == pfcode]
    idx = indices[indices == test_data["soup"].values[0]].index[0]
    print(5)
    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))
    print(6)
    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 코사인 유사도 기준으로 정렬된 데이터의 인덱스 정보 추출
    exhibit_indices = [i[0] for i in sim_scores]

    # 추출된 인덱스의 공연id와 종료 일자 추출 -> 데이터프레임으로
    rec_id = pre_pf[["mt20id", "prfpdto"]].iloc[exhibit_indices]

    today = datetime.datetime.now()
    res_list = []
    # 오늘 날짜와 비교하여 종료일이 더 늦는 공연을 res_list에 저장(n개 저장 시 break)
    for index, row in rec_id.iterrows():
        year, month, date = list(map(int, row["prfpdto"].split(".")))
        prfdate = datetime.datetime(year, month, date)
        if prfdate > today:
            res_list.append(row["mt20id"])
        if len(res_list) >= 5:
            break
    return res_list
