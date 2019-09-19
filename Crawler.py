from selenium import webdriver

class Crawler:

    def get_abs_value_naver(searchword):

        relatedKeywords = {}  # 연관 검색어 : [pc, mobile]
        publishVolumes = {} # blog : 발행량, cafe : 발행량, knwlgin : 발행량

        driver = webdriver.Chrome('/Users/yubin/ChromeDriver/chromedriver4')  # mac 나의 컴퓨터 기준으로 크롬 드라이버 저장된 위치, test시 수정해서 쓰세요
        driver.implicitly_wait(2)
        driver.get('http://surffing.net/')
        driver.find_element_by_xpath('//*[(@id = "saerchKeyword")]').send_keys(searchword)
        driver.find_element_by_class_name('key-btn').click()  # 자동 클릭처리

        results = driver.find_elements_by_xpath('//td')

        count = 0
        for result in results[:3]:
            count += 1

            if count % 3 == 1: # 월간 블로그 발행량
                publishVolumes['blog'] = result.text

            elif count % 3 == 2: # 월간 카페 발행량
                publishVolumes['cafe'] = result.text

            else: # 월간 지식인 발행량
                publishVolumes['knwlgin'] = result.text


        bufferKey = ''
        bufferPC = ''
        bufferM = ''

        count = 0
        for result in results[6:]:
            count += 1

            if count % 3 == 1: # 연관 검색어
                bufferKey = result.text

            elif count % 3 == 2: # 월간 검색수 PC
                bufferPC = result.text

            elif count % 3 == 0: # 월간 검색수 모바일
                bufferM = result.text

            relatedKeywords[bufferKey] = [bufferPC, bufferM]

        return relatedKeywords, publishVolumes


# test용 -- 지워질 코드
sw = '삼성'
rk, pb = Crawler.get_abs_value_naver(sw) # 여러개 return 했기 때문에 tuple로 반환하기 때문
# Crawler object 자체 함수,,
print(rk.keys()) # 연관 검색어만 뽑기
print(pb.values()) # 발행량 뽑기
print(pb) # dic 구조 확인





