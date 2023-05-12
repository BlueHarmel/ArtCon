from seleniumwire import webdriver
from seleniumwire.storage import RequestStorage
import chromedriver_autoinstaller as AutoChrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from artAddress import chromedriverAddress, URL, DB
from django.conf import settings
import datetime
import requests
from time import sleep
import json

li_item = []


def add_data(name, img, address, start, end, open_time, fee, homepage, x_coor, y_coor):
    dict1 = {
        "전시회명": name,
        "장소명": address,
        "시작일": start,
        "종료일": end,
        "운영시간": open_time,
        "요금": fee,
        "상세페이지 주소": homepage,
        "전시회 이미지 경로": img,
    }
    dict2 = {"장소명": address, "x": x_coor, "y": y_coor}
    li_item.append({"data1": dict1, "data2": dict2})


def save_data(dbpath):
    with open(dbpath, "a+", encoding="utf-8-sig") as f:
        json.dump(
            li_item,
            f,
            ensure_ascii=False,
            indent=2,
        )
    f.close()


def get_date():
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    return year, month, day


year, month, day = get_date()


def find_location(region):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    rest_api_key = settings.KAKAO_REST_API_KEY
    params = {"query": region}
    headers = {"Authorization": "KakaoAK " + rest_api_key}

    r = requests.get(url, params=params, headers=headers)

    if r.status_code == 200 and r.json()["documents"] != []:
        result_address = r.json()["documents"][0]
        result = result_address["y"], result_address["x"]
    elif r.json()["documents"] == []:
        result = "알수없음", "알수없음"
    else:
        result = "ERROR[" + str(r.status_code) + "]"
    return result


def seoul_crawl():
    global li_item
    li_item = []
    dbpath = DB[0]
    open(dbpath, "w").close()

    driver.get(url=URL[0])

    driver.implicitly_wait(2)
    driver.find_element(By.CSS_SELECTOR, "#s-sub").click()
    driver.find_element(
        By.CSS_SELECTOR, "#s-sub > option.subjCodeGroup-EXHIBITION"
    ).click()
    driver.find_element(By.CSS_SELECTOR, "#datepicker01").send_keys(
        year + Keys.TAB + month + day + Keys.TAB + year + Keys.TAB + month + day
    )
    driver.implicitly_wait(2)
    driver.find_element(
        By.CSS_SELECTOR, "#searchField > ul > li.clearfix.s3.sch > button.btn"
    ).click()
    sleep(2)

    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "#frm > div.event-list-wrap > div.paginationSet > ul > li.i.end > a",
        ).click()
        sleep(2)
        list_num = driver.find_element(
            By.CSS_SELECTOR, "#frm > div.event-list-wrap > div.paginationSet > ul"
        )
        num_li = int(
            list_num.find_elements(By.CSS_SELECTOR, "li")[-1].get_attribute("innerText")
        )
    except NoSuchElementException:
        list_num = driver.find_element(
            "#frm > div.event-list-wrap > div.paginationSet > ul"
        )
        num_li = len(list_num.find_elements(By.CSS_SELECTOR, "li"))

    driver.find_element(
        By.CSS_SELECTOR,
        "#frm > div.event-list-wrap > div.paginationSet > ul > li.i.first.disabled > a",
    ).click()
    sleep(2)

    for page_num in range(1, num_li + 1):
        if page_num > 2:
            page_num += 2
        if page_num > 1:
            driver.find_element(
                By.CSS_SELECTOR,
                f"#frm > div.event-list-wrap > div.paginationSet > ul > li:nth-child({page_num}) > a > span",
            ).click()
            sleep(1)

        item_num = driver.find_element(By.CSS_SELECTOR, "#dataList")
        item_li = len(item_num.find_elements(By.CSS_SELECTOR, "li"))

        for elem_num in range(1, item_li + 1):
            link = driver.find_element(
                By.CSS_SELECTOR, f"#dataList > li:nth-child({elem_num}) > a"
            ).get_attribute("href")
            driver.execute_script('window.open("https://google.com");')
            sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(link)
            req_url = link.split("?")[0]
            request = driver.wait_for_request(req_url)
            sleep(2)

            if request.response:
                res_code = request.response.body.decode("utf-8")
                lat_idx = res_code.find("var lat")
                x_coor = (
                    res_code[lat_idx : lat_idx + 70]
                    .split(";")[0]
                    .split("=")[1]
                    .lstrip(" '")
                    .rstrip("'")
                )
                y_coor = (
                    res_code[lat_idx : lat_idx + 70]
                    .split(";")[1]
                    .split("=")[1]
                    .lstrip(" '")
                    .rstrip("'")
                )

            driver.backend.storage.clear_requests()
            sleep(1)
            name = driver.find_element(
                By.CSS_SELECTOR,
                "#print > div.intro-top.clearfix > div.txt-box > div.event-title > h2",
            ).text
            image = driver.find_element(
                By.CSS_SELECTOR, "#print > div.intro-top.clearfix > div.img-box > img"
            ).get_attribute("src")
            address = driver.find_element(
                By.CSS_SELECTOR,
                "#print > div.intro-top.clearfix > div.txt-box > div.type-box > ul > li:nth-child(1) > div.type-td > span",
            ).text
            start, end = driver.find_element(
                By.CSS_SELECTOR,
                "#print > div.intro-top.clearfix > div.txt-box > div.type-box > ul > li:nth-child(2) > div.type-td > span",
            ).text.split(" ~ ")
            open_time = driver.find_element(
                By.CSS_SELECTOR,
                "#print > div.intro-top.clearfix > div.txt-box > div.type-box > ul > li:nth-child(3) > div.type-td > span",
            ).text
            fee = driver.find_element(
                By.CSS_SELECTOR,
                "#print > div.intro-top.clearfix > div.txt-box > div.type-box > ul > li:nth-child(5) > div.type-td > span",
            ).text
            try:
                homepage = driver.find_element(
                    By.CSS_SELECTOR,
                    "#print > div.intro-top.clearfix > div.txt-box > div.detail-btn > a",
                ).get_attribute("href")
            except NoSuchElementException:
                homepage = "없음"

            add_data(
                name,
                image,
                address,
                start,
                end,
                open_time,
                fee,
                homepage,
                x_coor,
                y_coor,
            )

            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            sleep(1)

        if page_num > 2:
            page_num -= 2
    save_data(dbpath)


def naver_crawl():
    global li_item
    li_item = []
    dbpath = DB[1]
    open(dbpath, "w").close()

    driver.get(url=URL[1])
    sleep(1)
    driver.implicitly_wait(2)
    driver.find_element(
        By.CSS_SELECTOR,
        "#main_pack > div.sc_new.cs_common_module.case_list.color_5._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_filter_tap > div > div > div > ul > li.tab.open > div > ul > li:nth-child(1) > a",
    ).click()

    tot_page = int(
        driver.find_element(
            By.CSS_SELECTOR,
            "#main_pack > div.sc_new.cs_common_module.case_list.color_5._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > span > span._total",
        ).text
    )
    for page_num in range(1, 10):
        for idx in range(1, 5):
            try:
                link = driver.find_element(
                    By.CSS_SELECTOR,
                    f"#mflick > div > div > div > div > div:nth-child({idx}) > div.data_area > div > div.title > div > strong > a",
                ).get_attribute("href")
            except NoSuchElementException:
                continue
            driver.execute_script('window.open("");')
            sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(link)

            name = driver.find_element(
                By.CSS_SELECTOR,
                "#main_pack > div.sc_new.cs_common_module.case_normal.color_5._kgs_art_exhibition > div.cm_top_wrap._sticky._custom_select._header > div.title_area._title_area > h2 > span.area_text_title > strong > a",
            ).text
            image = driver.find_element(
                By.CSS_SELECTOR,
                "#main_pack > div.sc_new.cs_common_module.case_normal.color_5._kgs_art_exhibition > div.cm_content_wrap > div > div > div.detail_info > a > img",
            ).get_attribute("src")
            start, end = driver.find_element(
                By.CSS_SELECTOR,
                "#main_pack > div.sc_new.cs_common_module.case_normal.color_5._kgs_art_exhibition > div.cm_content_wrap > div > div > div.detail_info > dl > div:nth-child(2) > dd",
            ).text.split(" ~ ")
            open_time = "알수 없음"
            fee = "알수 없음"
            homepage = driver.find_element(
                By.CSS_SELECTOR,
                "#main_pack > div.sc_new.cs_common_module.case_normal.color_5._kgs_art_exhibition > div.cm_content_wrap > div > div > div.detail_info > a",
            ).get_attribute("href")
            x_coor = "추후 추가"
            y_coor = "추후 추가"

            link = driver.find_element(
                By.CLASS_NAME,
                "place",
            ).get_attribute("href")
            driver.execute_script('window.open("");')
            sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(link)
            sleep(5)
            content = driver.find_element(By.CSS_SELECTOR, "#entryIframe")
            driver.switch_to.frame(content)
            address = driver.find_element(
                By.CSS_SELECTOR,
                "#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.tQY7D > div > a",
            ).text
            driver.switch_to.default_content()

            add_data(
                name,
                image,
                address,
                start,
                end,
                open_time,
                fee,
                homepage,
                x_coor,
                y_coor,
            )
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(
            By.CSS_SELECTOR,
            "#main_pack > div.sc_new.cs_common_module.case_list.color_5._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > a.pg_next.on",
        ).click()
        sleep(3)

    save_data(dbpath)


def interp_crawl():
    global li_item
    li_item = []
    dbpath = DB[2]
    open(dbpath, "w").close()

    driver.get(url=URL[2])

    driver.implicitly_wait(2)
    exhibition = driver.find_element(
        By.CSS_SELECTOR,
        "#wrapBody > div.sR_w726 > div.Rg_list > div.Ltview > div > div:nth-child(7) > div.Gp",
    )
    exhibitions = exhibition.find_elements(By.CLASS_NAME, "content")

    for e in exhibitions:
        link = (
            e.find_element(By.CLASS_NAME, "txt")
            .find_element(By.TAG_NAME, "a")
            .get_attribute("href")
        )

        driver.execute_script('window.open("");')
        sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link)
        sleep(1)

        name = driver.find_element(
            By.CSS_SELECTOR,
            "#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryTop > h2",
        ).text
        image = driver.find_element(
            By.CSS_SELECTOR,
            "#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > div > div.posterBoxTop > img",
        ).get_attribute("src")

        try:
            start, end = driver.find_element(
                By.CSS_SELECTOR,
                "#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li:nth-child(2) > div > p",
            ).text.split(" ~")
        except ValueError:
            start = driver.find_element(
                By.CSS_SELECTOR,
                "#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li:nth-child(2) > div > p",
            ).text
            end = "알수 없음"
        open_time = "알수 없음"
        try:
            driver.find_element(
                By.CSS_SELECTOR,
                "#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li.infoItem.infoPrice > div > ul > li.infoPriceItem.is-largePrice > a",
            ).send_keys(Keys.ENTER)
            fee = driver.find_element(
                By.CSS_SELECTOR,
                "#popup-info-price > div > div.popupBody > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2)",
            ).text
        except NoSuchElementException:
            fee = "알수 없음"
        homepage = driver.current_url
        x_coor = "추후 추가"
        y_coor = "추후 추가"
        driver.find_element(
            By.CSS_SELECTOR,
            "#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li:nth-child(1) > div > a",
        ).send_keys(Keys.ENTER)
        address = driver.find_element(
            By.CSS_SELECTOR,
            "#popup-info-place > div > div.popupBody > div > div.popPlaceInfo > p > span",
        ).text

        add_data(
            name,
            image,
            address,
            start,
            end,
            open_time,
            fee,
            homepage,
            x_coor,
            y_coor,
        )

        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        sleep(1)
    save_data(dbpath)


def yes_crawl():
    global li_item
    li_item = []
    dbpath = DB[3]
    open(dbpath, "w").close()

    driver.get(url=URL[3])

    driver.implicitly_wait(2)
    driver.find_element(
        By.CSS_SELECTOR,
        "body > div.content-min-wrap > div.area-division > a:nth-child(2)",
    ).click()
    driver.find_element(
        By.CSS_SELECTOR,
        "body > div.content-min-wrap > div.area-srch > div.area-srch-top > a",
    ).click()
    driver.find_element(
        By.CSS_SELECTOR,
        "body > div.content-min-wrap > div.area-srch > div.area-srch-bottom.on > div.area-srch-division > dl:nth-child(1) > dd > div:nth-child(9) > label",
    ).click()
    driver.find_element(
        By.CSS_SELECTOR,
        "body > div.content-min-wrap > div.area-srch > div.area-srch-bottom.on > div.area-srch-btns > a:nth-child(2)",
    ).click()
    sleep(2)
    exhibitions = driver.find_element(
        By.CSS_SELECTOR,
        "#ListCntText",
    ).text.split(
        "개"
    )[0]

    for idx in range(int(exhibitions)):
        exnum = idx % 5 + 1
        exline = 5 + int(idx / 5)
        driver.find_element(
            By.XPATH, f"/html/body/div[5]/div[{exline}]/a[{exnum}]"
        ).click()
        name = driver.find_element(
            By.CSS_SELECTOR, "#mainForm > div:nth-child(43) > div > div.rn-02 > p"
        ).text
        image = driver.find_element(
            By.CSS_SELECTOR,
            "#mainForm > div.renew-wrap.rw2 > div > div.rn-03 > div.rn-03-left > div.rn-product-imgbox > img",
        ).get_attribute("src")
        address = driver.find_element(By.ID, "TheaterAddress").text
        start, end = driver.find_element(
            By.CSS_SELECTOR,
            "#mainForm > div:nth-child(43) > div > div.rn-02 > div > p > span",
        ).text.split(" ~ ")
        open_time = "알수 없음"
        fee = driver.find_element(By.CSS_SELECTOR, "#mCSB_3_container").text
        homepage = driver.current_url
        x_coor = "추후 추가"
        y_coor = "추후 추가"

        add_data(
            name,
            image,
            address,
            start,
            end,
            open_time,
            fee,
            homepage,
            x_coor,
            y_coor,
        )

        driver.back()
        sleep(1)

    save_data(dbpath)


def mmca_crawl():
    global li_item
    li_item = []
    dbpath = DB[4]
    open(dbpath, "w").close()

    driver.get(url=URL[4])
    sleep(1)
    driver.implicitly_wait(2)
    pageling = driver.find_element(By.CSS_SELECTOR, "#pageDiv > nav")
    pagelist = pageling.find_elements(By.TAG_NAME, "a")
    pagelist.insert(
        0, pageling.find_element(By.CSS_SELECTOR, "#pageDiv > nav > strong")
    )

    for page in pagelist:
        page.click()
        exul = driver.find_element(By.CSS_SELECTOR, "#listDiv > ul")
        exlist = exul.find_elements(By.TAG_NAME, "li")

        for ex in exlist:
            ex.find_element(
                By.TAG_NAME,
                "a",
            ).click()
            sleep(1)
            name = driver.find_element(
                By.CSS_SELECTOR,
                "#content > div > div.heading.depth01.borderX > div:nth-child(1) > h3",
            ).text
            image = driver.find_element(
                By.CSS_SELECTOR,
                "#exhInfo > div.detailBody > div > div.bodySection.detailCont > div.contSlideWrap.exhibitionView > div > div > div.swiper-slide.swiper-slide-active > figure > img",
            ).get_attribute("src")
            address = driver.find_element(
                By.CSS_SELECTOR,
                "#exhInfo > div.detailBody > div > div.bodySection.detailCont > div.box.artInfo > ul:nth-child(1) > li:nth-child(3) > dl > dd > a",
            ).text
            start, end = driver.find_element(
                By.CSS_SELECTOR,
                "#exhInfo > div.detailBody > div > div.bodySection.detailCont > div.box.artInfo > ul:nth-child(1) > li:nth-child(1) > dl > dd",
            ).text.split(" ~ ")
            open_time = "알수 없음"
            fee = driver.find_element(
                By.CSS_SELECTOR,
                "#exhInfo > div.detailBody > div > div.bodySection.detailCont > div.box.artInfo > ul:nth-child(1) > li:nth-child(4) > dl > dd",
            ).text
            homepage = driver.current_url
            x_coor = "알수 없음"
            y_coor = "알수 없음"
            driver.back()

            add_data(
                name,
                image,
                address,
                start,
                end,
                open_time,
                fee,
                homepage,
                x_coor,
                y_coor,
            )

            sleep(1)
    save_data(dbpath)


chrome_Ver = AutoChrome.get_chrome_version()
AutoChrome.install(True)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")  # 브라우저가 최대화된 상태로 실행됩니다.
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"
)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(chromedriverAddress, options=chrome_options)
driver.set_window_size(1920, 1280)
driver.implicitly_wait(2)

# seoul_crawl()
naver_crawl()
# interp_crawl()
# yes_crawl()
# mmca_crawl()
