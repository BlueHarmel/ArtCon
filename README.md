***

## ArtCon

한국외대 GBT학부 캡스톤 프로젝트

### 프로젝트 소개

**ArtCon**은 공연/전시/예술 행사 정보를 수집, 추천, 공유하는 웹 플랫폼입니다. Django 기반 백엔드와 다양한 크롤러, 추천 시스템, 사용자 인증/게시판/리뷰/찜 기능을 포함합니다.

***

### 주요 기능

- **전시/공연 정보 실시간 크롤링 및 데이터베이스화**
  - 다양한 공연·전시 사이트에서 데이터 자동 수집(Selenium, BeautifulSoup 사용)
  - 크롤링된 정보를 DB에 자동 저장하여 최신 일정 및 상세정보 제공

- **사용자별 맞춤 추천 시스템(TF-IDF 등 활용)**
  - 공연·전시명, 출연진, 제작진 등 주요 정보를 기반으로 사용자 관심사 추천(코사인 유사도 활용)
  - 찜 목록, 과거 리뷰 데이터를 반영하여 개인화 추천 제공
  - 추천시스템 소스: scikit-learn, pandas, recommend_test.py 등

- **공연/전시 리뷰, 평점, 찜하기 기능**
  - 사용자별 평점 및 텍스트 리뷰 작성/수정/좋아요 기능 제공
  - 공연·전시 찜 목록 관리 및 리뷰/평점·찜 기반 맞춤 추천 연동

- **게시판 및 커뮤니티(질문/자유 게시판)**
  - 공연/전시에 대한 자유 게시글·Q&A·토론 가능(댓글, 좋아요 기능 포함)
  - 커뮤니티 내 활동/의견 교환 지원(별도 신고/관리 시스템 연결 가능)

- **회원가입/로그인/권한 관리**
  - Django 인증 및 권한 관리를 통해 회원가입, 로그인, 비밀번호 찾기, 권한 변경 지원
  - 관리자/일반 사용자 구분, 세션 및 보안 강화

- **검색 및 위치 기반 정보 제공**
  - 공연·전시 정보 키워드 및 지역 기반 검색
  - Kakao API 활용 공연·전시 위치/지도, 주소 기반 필터 검색 지원

***

### 기술 스택

- **Backend:** Python, Django, MySQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Crawler:** Selenium, BeautifulSoup, Pandas, Crawling scripts (ex. infoCrawler.py)
- **머신러닝(추천):** scikit-learn, pandas
- **기타:** Django Summernote(에디터), Django Social Share

***

### 프로젝트 구조

- `ArtCon/`: Django 메인 프로젝트
  - `authpage_app/`: 회원/인증/권한 관리
  - `boardpage_app/`: 리뷰 및 게시판(댓글/좋아요 등)
  - `exhibpage_app/`: 전시/공연 정보 관리, 추천 기능
  - `mainpage_app/`: 메인페이지 및 홈 뷰
  - `recompage_app/`: 추천 시스템 구성
  - `searchpage_app/`: 통합 검색 기능
  - `static/`, `templates/`: CSS, JS, HTML 템플릿
- `ArtCon Crawler/`: infoCrawler.py, contentFilter.py 등 공연/전시 크롤러

***

### 실행 방법

1. Python 3 및 Django, MySQL 환경 준비
2. 의존 패키지 설치
   ```
   pip install -r piplist.txt
   ```
3. DB 및 Django 마이그레이션 설정
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. 서버 실행
   ```
   python manage.py runserver
   ```

***

### 데이터/크롤러 안내

- `ArtCon Crawler` 폴더 내 infoCrawler.py, chromedriver, contentFilter.py 등 각종 공연정보사이트 데이터 크롤러/필터 존재
- 추천시스템: recommender_test.py, pre_pf.csv, test.npz 등 선호 기반 공연 추천

***

### 팀원

- BlueHarmel (팀장)
- JinbeeLee
- JNyum
- castle_chan

***
