import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from sklearn.metrics.pairwise import linear_kernel
import re
from scipy import sparse
import numpy as np

pre_pf = pd.read_csv("ArtCon Crawler/p_pre.csv", encoding="utf-8")
now_pf = pd.read_csv("ArtCon Crawler/p_now.csv", encoding="utf-8")
post_pf = pd.read_csv("ArtCon Crawler/performance_post_detail.csv", encoding="utf-8")

merged_pf = pd.concat([pre_pf, now_pf])
merged_pf = pd.concat([merged_pf, post_pf])
print(len(pre_pf), len(now_pf), len(merged_pf))


# 'prfcast' 및 'prfcrew' 열의 데이터 처리
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


for feature in ["prfnm", "prfcast", "prfcrew"]:
    merged_pf[feature] = merged_pf[feature].apply(process_str)


def create_soup(x):
    return (
        " ".join(x["prfnm"])
        + " "
        + " ".join(x["prfcast"])
        + " "
        + " ".join(x["prfcrew"])
    )


merged_pf["soup"] = merged_pf.apply(create_soup, axis=1)
okt = Okt()
stopwords = ["을", "를", "이", "가", "은", "는"]

tfidf_vectorizer = TfidfVectorizer(tokenizer=okt.morphs, stop_words=stopwords)
tfidf_matrix = tfidf_vectorizer.fit_transform(merged_pf["soup"])
print(tfidf_matrix)
sparse.save_npz("test.npz", tfidf_matrix)
