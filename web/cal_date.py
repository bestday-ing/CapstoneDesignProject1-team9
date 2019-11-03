import datetime

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