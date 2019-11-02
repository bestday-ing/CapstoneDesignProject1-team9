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
    driver = webdriver.Chrome(executable_path=r"C:\\Program Files (x86)\\Google\\chromedriver.exe", options=options)
    driver.implicitly_wait(2)

    # 크롤링 주소
    driver.get('https://trends.google.co.kr/trends/?geo=KR')

    # 작동되었는지 확인
    assert "트렌드" in driver.title

    # 목표 단어 타이핑 및 검색
    driver.find_element_by_id('input-1').send_keys(word)
    driver.find_element_by_id('input-1').send_keys(Keys.ENTER)

    # 모든 차트가 로드 될 때까지 대기
    sleep(1)

    # 차트 찾기
    lst = driver.find_elements_by_css_selector(".widget-actions-item.export")

    # 차트 3개 중 가장 위의 차트가 가장 먼저 로드되는 경우, 0번에 저장됨(일반적)
    lst[0].click()
    
    # 다운로드 대기
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
    normval = random.randrange(140000, 220000)

    for elem in y:
        z.append(round(normval * (elem / normvalratio)))

    return z

# 목표 단어
word = "노트북"
multiTimeLinePath = "C:\\Users\\82108\\Downloads\\multiTimeLine.csv"
geoMapPath = "C:\\Users\\82108\\Downloads\\geoMap.csv"

t1 = Thread(target = crawlingAndDownloading, args = (word, multiTimeLinePath, ))
t1.start()

t1.join()
x, y = listingAndDeleting(multiTimeLinePath, geoMapPath)

z = rgoogleAndCal(y)

print(z)
