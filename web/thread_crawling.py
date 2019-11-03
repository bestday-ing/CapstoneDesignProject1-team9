from queue import Queue
from threading import Thread
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from threading import Thread
from time import sleep
import csv
import random
import os

def crawlingAndDownloading(word, path):
    # 크롤링 옵션
    options = Options()
    options.add_experimental_option('detach', True)
    #options.add_argument('--headless')
    options.add_argument('--window-position=0,0')

    # 주소 변경 필요!! 크롬 드라이버 설정
    driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')


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

def rgoogleAndCal(y):
    z = list()
    normvalratio = sum(y) / len(y)
    random.seed(420)
    normval = random.randrange(140000, 220000)

    for elem in y:
        z.append(round(normval * (elem / normvalratio)))

    return z


def get_abs_value_google(searchword):
    # 목표 단어
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

    google = {
        'graphData': graphData
        # 'related': rk 나중에 연관 검색어
    }

    return google

# thread 2
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
    # json 만들기 (1) dictionary (2) 1을 json으로 변환
    daum = {
        'count' : 200000,
        'related' : realted
    }

    '''
    test_json_str = json.dumps(test)
    test_json_data = json.loads(test_json_str)
    print(test_json_data)
    print(test_json_data["daum"]["related"]) # 속성
    '''
    return daum # dictionay 던짐


# get_abs_value_and_related_keywords_daum("삼성")


def get_abs_value_naver(searchword):
    try:
        driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')  # 맥 경로, 불필요시 주석 처리바람
    except:
        driver = webdriver.Chrome('./chromedriver_77.exe')  # 버전에 따라 수정해서
    wait = WebDriverWait(driver, 20)
    relatedKeywords = {}  # 연관 검색어 : [pc, mobile]
    publishVolumes = {}  # blog : 발행량, cafe : 발행량, knwlgin : 발행량

    # driver = webdriver.Chrome('C:\\Python\\chromedriver\\chromedriver_77.exe')  # 버전에 따라 수정해서
    # driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')  # 버전에 따라 수정해서
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



import os
import sys
import pandas as pd
import json
import urllib.request
import datetime
# from rpy2.robjects import r


# 주어진 구간에 대한 검색함수. json -> dict -> list 형식으로 변환하여 재구성해서 반환
def SectionSearch(StartDate, EndDate, Keyword, DeviceType):
    client_id = "QqTTJVe3ttjxiFKxy6gi"
    client_secret = "GqJHHxrHRX"
    url = "https://openapi.naver.com/v1/datalab/search"
    body = "{\"startDate\":\"" + StartDate + "\",\"endDate\":\"" + EndDate + "\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"-\",\"keywords\":[\"" + Keyword + "\"]}],\"device\":\"" + DeviceType + "\",\"ages\":[\"1\",\"2\"],\"gender\":\"\"}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    request.add_header("Content-Type", "application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        obj = json.loads(response_body)
        Result = obj['results']
        Datadict = Result[0]['data']
        DatalistTuple = []
        for a in Datadict:
            DatalistTuple.append(list(a.items()))
        Datalist = []
        for b in DatalistTuple:
            Datalist.append([b[0][1], b[1][1]])
        # 반환되는 Datalist는 [[기간1, 비율], [기간2, 비율], ... ] 로 구성, 기간은 1달단위
        return Datalist
    else:
        print("Error Code:" + rescode)
        return []


def isLeapYear(year):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def lastDay(year, month):
    DayList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if isLeapYear(year):
        DayList[1] = 29
    return DayList[month - 1]


# 현재 시간 기준 바로 전 달의 마지막 날 ex) '2019-08-31' 구하기
def FindRecentMonth():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    # 좀 더 효율적으로 하는 함수 구해줄 분 구합니다 파이썬을 잘 몰라서.. 진짜 막코딩해놨어요
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    RecentMonth = str(year) + '-'
    if month >= 10:
        RecentMonth += str(month)
    else:
        RecentMonth += '0' + str(month)
    RecentMonth += '-' + str(lastDay(year, month))

    return RecentMonth


# thread 1
# 최종적으로 검색할 것 입력하면 기간, 비율, 검색량으로

def search_naver(searchword): # 네이버 검색
    # 17년 1월 ~ 4월 검색한다 치면
    # 17년 1월 ~ 현재 시점의 가장 최근 달까지 구하고
    # 가장 최근 달의 진짜 검색량을 바탕으로
    # (최근검색량 / 최근달 비율) * 검색량 구할 달 해서
    # 17년 1월 ~ 4월의 월간 검색량을 구하도록

    # 시작 범위
    StartDate = "2016-01-01"
    # 끝 범위
    EndDate = "2018-11-30"
    # 검색어
    Keyword = searchword
    # "pc" or "mo" or 비워두면("") 둘다
    DeviceType = ""

    # Searchword = read_in()
    # Keyword = Searchword["keyword"]
    # Keyword = sys.argv[1]

    try:
        Keyword = sys.argv[1]
    except:
        Keyword = "치킨"

    try:
        StartDate = sys.argv[2]
    except:
        StartDate = "2016-01-01"

    try:
        EndDate = sys.argv[3]
    except:
        EndDate = FindRecentMonth()
    
    FullDatalist = SectionSearch(StartDate, FindRecentMonth(), Keyword, DeviceType)
    # 실제 최근 1달 검색량은 나중에 구하는 것으로 (현재는 데이터가 없어서 1000으로 둠)

    rk, pb = get_abs_value_naver(Keyword) # 둘 다 dictionary

    # 숫자 , 있는 거 parsing
    for k in rk.keys():
        for i in range(0, 2):
            buff = rk[k][i].split(",")
            number = ''
            for num in buff:
                number += num
            rk[k][i] = number

    RecentRealCount = int(rk[Keyword][0]) + int(rk[Keyword][1])
    FullDatalist.reverse()
    RealCountRatio = FullDatalist[0][1]
    FullDatalist.reverse()
    FinalDatalist = []
    for i in FullDatalist:
        if i[0] > EndDate:
            break
        i.append(RecentRealCount * i[1] / RealCountRatio)
        FinalDatalist.append(i)
    # FinalDatalist에는 [[기간1, 비율1, 검색량1], [기간2, 비율2, 검색량2], ... ] 로 구성, 기간은 1달 단위
    # json 만들기 (1) dictionary (2) 1을 json으로 변환
    '''
    period = []
    ratio = []
    count = []
    for list in FinalDatalist:
        period.append(list[0])
        ratio.append(list[1])
        count.append(list[2])

    graphData = {
        'period' : period,
        'ratio' : ratio,
        'count' : count
    }
    '''
    naver = {
        'graphData' : FinalDatalist,
        'related' : rk
    }

    '''
    test_json_str = json.dumps(test)
    print(test_json_str)
    test_json_data = json.loads(test_json_str)
    print(test_json_data)
    print(test_json_data["naver"]["graphData"]) # 속성
    print(test_json_data["naver"]["related"])  # 속성
    '''
    return naver # dictionay 던짐





from queue import Queue
from threading import Thread
import time
from selenium import webdriver


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':
    keyword = sys.argv[1]
    final = {}
    final["daum"] = get_related_keywords_daum(keyword)
    final["naver"] = search_naver(keyword)
    final["google"] = get_abs_value_google(keyword)
    final_json_str = json.dumps(final)
    print(final_json_str)
    
    '''
    result_queue = Queue()
    keyword = sys.argv[1]
    # keyword = "삼성"
    startDate = ""
    endDate = ""

    # We create two threads and pass shared queue to both of them.
    t1 = Thread(target=get_abs_value_and_related_keywords_daum, args=(result_queue, keyword))
    t2 = Thread(target=search_naver, args=(result_queue, keyword))

    # Starting threads...
  #  print("Start: %s" % time.ctime())
    t1.start()
    t2.start()

    # Waiting for threads to finish execution...
    t1.join()
    t2.join()
   # print("End:   %s" % time.ctime())

    final = {}

    # After threads are done, we can read results from the queue.
    while not result_queue.empty():
        result = result_queue.get()
        naver = result.get("naver")
        if naver:
            final["naver"] = result["naver"]
        else:
            final["daum"] = result["daum"]

      #  print("final result is ")
      #  print(final)

    final_json_str = json.dumps(final)
    print(final_json_str)
    '''

