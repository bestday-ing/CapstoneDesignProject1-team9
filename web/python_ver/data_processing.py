from Crawler import *
from cal_date import *
from openAPI import naverAPI_section_search
import sys
import json


def search_naver(searchword, StartDate, EndDate):
    # 17년 1월 ~ 4월 검색한다 치면
    # 17년 1월 ~ 현재 시점의 가장 최근 달까지 구하고
    # 가장 최근 달의 진짜 검색량을 바탕으로
    # (최근검색량 / 최근달 비율) * 검색량 구할 달 해서
    # 17년 1월 ~ 4월의 월간 검색량을 구하도록

    # 검색어
    Keyword = searchword
    # "pc" or "mo" or 비워두면("") 둘다
    DeviceType = ""
    FullDatalist = naverAPI_section_search(StartDate, FindRecentMonth(), Keyword, DeviceType) # 배열
    # 실제 최근 1달 검색량은 나중에 구하는 것으로 (현재는 데이터가 없어서 1000으로 둠)

    rk, pb = get_abs_value_and_related_keywords_naver(Keyword)  # 둘 다 dictionary

    ''' pre processing '''  # 숫자 ',' 있는 거 parsing
    for k in rk.keys():
        for i in range(0, 2):
            buff = rk[k][i].split(",")
            number = ''
            for num in buff:
                number += num
            try:
                rk[k][i] = int(number)
            except:
                number = ''
                filter = rk[k][i].split(" ")
                for num in filter:
                    if(num == "미만"): # 10 '미만'인 경우 처리
                        num = "/2"
                    number += num
                rk[k][i] = eval(number)
        rk[k].append(rk[k][0]+rk[k][1])

    # 상대 비율을 통한 절대값 계산을 모듈화하면 좋을 듯 구글도 쓰고~ 네이버도 쓰고~
    first = list(rk.keys())[0]
    RecentRealCount = int(rk[first][0]) + int(rk[first][1])
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
    # 최종적으로 검색할 것 입력하면 기간, 비율, 검색량으로

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
    ''' sorting '''
    searchword_specific = rk[first]
    del rk[first]
    sorted_rk = sorted(rk.items(), key=lambda x: x[1][2], reverse=True)
    newrk = {}
    for keyword in sorted_rk:
        newrk[keyword[0]] = [keyword[1][0], keyword[1][1]]
    # print(newrk)

    naver = {
        'graphData': FinalDatalist,
        'searchword': searchword_specific,
        'related': newrk
    }
    return naver  # dictionay 던짐

def search_google(searchword):  # 네이버 검색

    graphData = get_abs_value_google(keyword)
    # rk = get_related_keywords_google(keyword)

    google = {
        'graphData': graphData
        # 'related': rk 나중에 연관 검색어
    }

    return google  # dictionay 던짐


def search_daum(searchword):  # 네이버 검색

    rk = get_related_keywords_daum(keyword)
    # count = get_abs_value_daum(keyword)
    count = 1000000 # 일단 임의의 값 나중에 없앨까 싶다.

    daum = {
        'count' : count,
        'related' : rk
    }

    return daum  # dictionay 던짐



if __name__ == '__main__':
    keyword = sys.argv[1]
    try:
        startDate = sys.argv[2]
        if(startDate=="undefined"):
            # startDate = "2016-01-01"
            startDate = oneYearsAgo()
    except:
        startDate =  oneYearsAgo()

    try:
        endDate = sys.argv[3]
        if (endDate == "undefined"):
            endDate = FindRecentMonth()
    except:
        endDate = FindRecentMonth()

    final = {}
    final["daum"] = search_daum(keyword)
    final["naver"] = search_naver(keyword, startDate, endDate)
    final["google"] = {}
    final_json_str = json.dumps(final)
    print(final_json_str)
    
    ''' thread
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

