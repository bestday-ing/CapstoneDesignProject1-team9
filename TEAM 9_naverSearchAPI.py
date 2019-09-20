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
    body = "{\"startDate\":\"" + StartDate + "\",\"endDate\":\"" + EndDate + "\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"-\",\"keywords\":[\"" + Keyword + "\"]}],\"device\":\"" + DeviceType + "\",\"ages\":[\"1\",\"2\"],\"gender\":\"\"}";

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        obj = json.loads(response_body)
        Result = obj['results']
        Datadict = Result[0]['data']
        DatalistTuple = []
        for a in Datadict:
            DatalistTuple.append(list(a.items()))
        Datalist =[]
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
    if month >= 10 :
        RecentMonth += str(month)
    else:
        RecentMonth += '0' + str(month)
    RecentMonth += '-' + str(lastDay(year, month))

    return RecentMonth

# 최종적으로 검색할 것 입력하면 기간, 비율, 검색량으로
def Search(StartDate, EndDate, Keyword, DeviceType):
    # 17년 1월 ~ 4월 검색한다 치면
    # 17년 1월 ~ 현재 시점의 가장 최근 달까지 구하고
    # 가장 최근 달의 진짜 검색량을 바탕으로
    # (최근검색량 / 최근달 비율) * 검색량 구할 달 해서
    # 17년 1월 ~ 4월의 월간 검색량을 구하도록
    FullDatalist = SectionSearch(StartDate, FindRecentMonth(), Keyword, DeviceType)
    # 실제 최근 1달 검색량은 나중에 구하는 것으로 (현재는 데이터가 없어서 1000으로 둠)
    RecentRealCount = 1000
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
    SaveExcel(FinalDatalist)

# .csv파일 저장함수
def SaveExcel(Datalist):
    data = pd.DataFrame(Datalist)
    data.columns = ['Period', 'ratio', 'count']
    data.to_csv('Test.csv', encoding='cp949')


# 시작 범위
StartDate = "2016-01-01"
# 끝 범위
EndDate = "2018-11-30"
# 검색어
Keyword = "검색어"
# "pc" or "mo" or 비워두면("") 둘다
DeviceType = ""

Search(StartDate, EndDate, Keyword, DeviceType)