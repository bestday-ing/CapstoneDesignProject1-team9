
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from threading import Thread
from time import sleep
import csv
import random
import os



''' JSON 인코딩 디코딩
    test_json_str = json.dumps(test) # test가 dictionary 일 때 이렇게 json format string 만들 수 있음 
    test_json_data = json.loads(test_json_str) #json format string 을 JSON 객체로 만들기
    print(test_json_data)
    print(test_json_data["daum"]["related"]) # 속성 따라서 값 뽑아 내기
'''


''' 다음 '''
def get_abs_value_daum(searchword): # 광고주 로그인 세션 유지하는 방향으로 생각해보기
    try:
        driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')  # 맥 경로, 불필요시 주석 처리바람
    except:
        driver = webdriver.Chrome('./chromedriver_77.exe')  # 버전에 따라 수정해서
    wait = WebDriverWait(driver, 20)

    driver.get('https://clix.biz.daum.net/ad/proposal/keyword')
    driver.find_element_by_xpath('//*[(@id = "userId")]').send_keys("anfidthtn")
    driver.find_element_by_xpath('//*[(@id = "userPw")]').send_keys("asdf;lkj")
    driver.find_element_by_class_name('btn_comm2.btn_login').click()  # 자동 클릭처리
    # driver.implicitly_wait(2)
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[(@id = "proposalSearchKeyword")]'))
    )
    driver.find_element_by_xpath('//*[(@id = "proposalSearchKeyword")]').send_keys(searchword)
    # driver.find_element_by_xpath('//*[(@id = "proposalSearchDevice")]').send_keys(searchword) # 모바일도 필요한데,, 지금은 PC만 받는 상태
    driver.find_element_by_class_name('btn_comm.btn_inquiry').click()  # 자동 클릭처리
    # driver.implicitly_wait(10)
    # wait for the page to load
    wait.until(
        EC.presence_of_element_located((By.XPATH, '''//*[@class= "txt_ar"]'''))
    )
    abs_value = driver.find_element_by_xpath('''//*[@class= "txt_ar"]''')
    abs_value = abs_value.text

    buff = abs_value.split(",")
    number = ''
    for num in buff:
        number += num

    return int(number)

def get_related_keywords_daum(searchword): # 검색량 뽑아내는거
    try:
        driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')  # 맥 경로, 불필요시 주석 처리바람
    except:
        driver = webdriver.Chrome('./chromedriver_77.exe')  # 버전에 따라 수정해서
    wait = WebDriverWait(driver, 20)

    driver.get('https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&q='+searchword) #연관 검색어 출력
    results = driver.find_elements_by_xpath('//a[@class= "keyword"]')
    realted = []
    for i in results[:int(len(results)/2)]:
        if(i.text):
            realted.append(i.text)

    return realted # array 던짐

# get_abs_value_and_related_keywords_daum("삼성")


''' 네이버 '''
def get_abs_value_and_related_keywords_naver(searchword):
    try:
        driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')  # 맥 경로, 불필요시 주석 처리바람
    except:
        driver = webdriver.Chrome('./chromedriver_77.exe')  # 버전에 따라 수정해서
    wait = WebDriverWait(driver, 20)

    relatedKeywords = {}  # 연관 검색어 : [pc, mobile]
    publishVolumes = {}  # blog : 발행량, cafe : 발행량, knwlgin : 발행량

    driver.get('http://surffing.net/')
    driver.find_element_by_xpath('//*[(@id = "saerchKeyword")]').send_keys(searchword)
    driver.find_element_by_class_name('key-btn').click()  # 자동 클릭처리
    # driver.implicitly_wait(2)
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//td'))
    )
    results = driver.find_elements_by_xpath('//td')

    count = 0
    for result in results[:3]:
        count += 1

        if count % 3 == 1:  # 월간 블로그 발행량
            publishVolumes['blog'] = result.text

        elif count % 3 == 2:  # 월간 카페 발행량
            publishVolumes['cafe'] = result.text

        else:  # 월간 지식인 발행량
            publishVolumes['knwlgin'] = result.text

    bufferKey = ''
    bufferPC = ''
    bufferM = ''

    count = 0
    for result in results[6:]:
        count += 1

        if count % 3 == 1:  # 연관 검색어
            bufferKey = result.text

        elif count % 3 == 2:  # 월간 검색수 PC
            bufferPC = result.text

        elif count % 3 == 0:  # 월간 검색수 모바일
            bufferM = result.text

        relatedKeywords[bufferKey] = [bufferPC, bufferM]

    print("성공")
    return relatedKeywords, publishVolumes


''' 구글 '''
def get_abs_value_google(searchword): # 경로 문제 있음. 모든 컴퓨터에서 열 수 있도록. 크롬에서 다운할 때 폴더 지정 같은 처리가 필요할 듯

    word = searchword
    multiTimeLinePath = "/Users/yubin/Downloads/multiTimeLine.csv"
    geoMapPath = "/Users/yubin/Downloads/geoMap.csv"

    t1 = Thread(target=crawlingAndDownloading, args=(word, multiTimeLinePath,))
    t1.start()

    t1.join()
    x, y = listingAndDeleting(multiTimeLinePath, geoMapPath)

    z = rgoogleAndCal(y)

    graphData = {
        'period': x,
        'count': z
    }

    return graphData

def crawlingAndDownloading(word, path):
    # 크롤링 옵션
    options = Options()
    options.add_experimental_option('detach', True)
    #options.add_argument('--headless')
    options.add_argument('--window-position=0,0')

    try:
        driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')  # 맥 경로, 불필요시 주석 처리바람
    except:
        driver = webdriver.Chrome('./chromedriver_77.exe')  # 버전에 따라 수정해서

    # 크롤링 주소
    driver.get('https://trends.google.co.kr/trends/?geo=KR')

    # 작동되었는지 확인
    assert "트렌드" in driver.title

    # 목표 단어 타이핑 및 검색
    driver.find_element_by_id('input-254').send_keys(word)
    driver.find_element_by_id('input-254').send_keys(Keys.ENTER)
    driver.implicitly_wait(2)
    # 모든 차트가 로드 될 때까지 대기
    sleep(1)

    # 차트 찾기
    lst = driver.find_elements_by_css_selector(".widget-actions-item.export")

    # 차트 3개 중 가장 위의 차트가 가장 먼저 로드되는 경우, 0번에 저장됨(일반적)
    lst[0].click()

    sleep(1)

    # 만약 두 번째 차트가 먼저 로드된 경우, 추가 다운로드를 통해 첫 번째 차트를 다운로드
    if os.path.isfile(path) == False:
        lst = driver.find_elements_by_css_selector(".widget-actions-item.export")
        lst[1].click()

def listingAndDeleting(corpath, wrgpath):
    # 다운로드 시간을 위한 대기
    sleep(1)

    # 주소 변경 필요!! 첫 번째 차트가 다운 되었는지 다운로드 파일 체크 및 열기
    if os.path.isfile(corpath):
        fi = open(corpath, mode='r', encoding='utf-8')
    else:
        print("Error!")

        # 두 번째 차트만 로드 된 경우
        if os.path.isfile(wrgpath):
            os.remove(wrgpath)

        exit(1)

    # csv.reader
    rdr = csv.reader(fi)

    # x에 날짜 저장, y에 상대빈도 저장
    x = list()
    y = list()

    # header 및 빈칸 제외 규칙으로 데이터 append
    for line in rdr:
        if len(line) > 1 and line[0] != '주':
            x.append(line[0])
            y.append(int(line[1]))

    # 콘솔 출력
    #print(x)
    #print(y)

    # 다운로드 파일 닫기
    fi.close()

    # 주소 변경 필요!! #다운로드 파일 삭제
    os.remove(corpath)

    # 두 번째 차트가 다운된 경우
    if os.path.isfile(wrgpath):
        os.remove(wrgpath)

    return (x, y)

def rgoogleAndCal(y): # 절대값을 투영한 상대비율의 절대지표 계산
    z = list()
    normvalratio = sum(y) / len(y)
    random.seed(420)
    normval = random.randrange(140000, 220000)

    for elem in y:
        z.append(round(normval * (elem / normvalratio)))

    return z



