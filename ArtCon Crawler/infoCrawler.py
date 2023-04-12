# from selenium import webdriver
from seleniumwire import webdriver
from seleniumwire.storage import RequestStorage
import chromedriver_autoinstaller as AutoChrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from artAddress import chromedriverAddress, URL, kakao_rest_api_key
import datetime
import requests
from time import sleep
import json


def save_data(name, img, address, start, end, open_time, fee, homepage, x_coor, y_coor):
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

    with open("./data.json", "a+", encoding="utf-8-sig") as f:
        json.dump({"data1": dict1, "data2": dict2}, f, ensure_ascii=False, indent=4)
    f.close()


def get_date():
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    return year, month, day


year, month, day = get_date()


# def find_location(region):
#    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
#    rest_api_key = kakao_rest_api_key
#    params = {"query": region}
#    headers = {"Authorization": "KakaoAK " + rest_api_key}
#
#    r = requests.get(url, params=params, headers=headers)
#
#    if r.status_code == 200 and r.json()["documents"] != []:
#        result_address = r.json()["documents"][0]
#        result = result_address["y"], result_address["x"]
#    elif r.json()["documents"] == []:
#        result = "알수없음", "알수없음"
#    else:
#        result = "ERROR[" + str(r.status_code) + "]"
#    return result


def info_crawl():
    open("./data.json", "w").close()

    chrome_Ver = AutoChrome.get_chrome_version()
    AutoChrome.install(True)
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
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

            save_data(
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


info_crawl()
