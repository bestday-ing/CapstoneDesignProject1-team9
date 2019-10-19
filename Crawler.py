from selenium import webdriver


def get_abs_value_naver(searchword):

    relatedKeywords = {}  # 연관 검색어 : [pc, mobile]
    publishVolumes = {} # blog : 발행량, cafe : 발행량, knwlgin : 발행량

    #driver = webdriver.Chrome('C:\\Python\\chromedriver\\chromedriver_77.exe')  # 버전에 따라 수정해서 
    driver = webdriver.Chrome('./chromedriver_77.exe')  # 버전에 따라 수정해서 
    driver.get('http://surffing.net/')
    driver.find_element_by_xpath('//*[(@id = "saerchKeyword")]').send_keys(searchword)
    driver.find_element_by_class_name('key-btn').click()  # 자동 클릭처리
    driver.implicitly_wait(2)
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


# #test용 -- 지워질 코드
# sw = '삼성'
# rk, pb = Crawler.get_abs_value_naver(sw) # 여러개 return 했기 때문에 tuple로 반환하기 때문
# #Crawler object 자체 함수,,
# print(rk.keys()) # 연관 검색어만 뽑기
# print(pb.values()) # 발행량 뽑기
# print(pb[sw]) # 발행량 뽑기
# print(rk[sw]) # 발행량 뽑기
# print(pb) # dic 구조 확인
# import sys, json
# from selenium import webdriver
# def read_in(): 
#     #print(sys.stdin.readline())
#     return json.loads(sys.stdin.readline())

# def get_abs_value_naver():
#     #searchword = json.loads(read_in(), encoding='utf-8')
#     searchword = read_in()

    
#     #searchword = json.dumps(read_in(), ensure_ascii=False)
    
#     relatedKeywords = {}  # 연관 검색어 : [pc, mobile]
#     publishVolumes = {} # blog : 발행량, cafe : 발행량, knwlgin : 발행량
    
#     driver = webdriver.Chrome('C:/Python/2/chromedriver.exe')  # 버전에 따라 수정해서 
#     driver.get('http://surffing.net/')
#     driver.find_element_by_xpath('//*[(@id = "saerchKeyword")]').send_keys(searchword["keyword"])
#     driver.find_element_by_class_name('key-btn').click()  # 자동 클릭처리
#     driver.implicitly_wait(2)
#     results = driver.find_elements_by_xpath('//td')

#     # while True:
#     #     num = 1

#     count = 0
#     for result in results[:3]:
#         count += 1

#         if count % 3 == 1: # 월간 블로그 발행량
#             publishVolumes['blog'] = result.text

#         elif count % 3 == 2: # 월간 카페 발행량
#             publishVolumes['cafe'] = result.text

#         else: # 월간 지식인 발행량
#             publishVolumes['knwlgin'] = result.text


#     bufferKey = ''
#     bufferPC = ''
#     bufferM = ''

#     count = 0
#     for result in results[6:]:
#         count += 1

#         if count % 3 == 1: # 연관 검색어
#             bufferKey = result.text

#         elif count % 3 == 2: # 월간 검색수 PC
#             bufferPC = result.text

#         elif count % 3 == 0: # 월간 검색수 모바일
#             bufferM = result.text

#         relatedKeywords[bufferKey] = [bufferPC, bufferM]
#     #return publishVolumes
#     return relatedKeywords, publishVolumes
# if __name__ == '__main__':
#     get_abs_value_naver()


