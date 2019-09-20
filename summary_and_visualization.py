from rpy2.robjects import r
from matplotlib import pyplot as plt
import pandas as pd

def printSummary(path):
    r.assign('path', path)
    r('data <- read.csv(path, header = T)')
    r('print(summary(data[,2:4]))')

    data = pd.read_csv(path)

    feature = ['Period', 'ratio', 'count']

    data_pd = data[feature]

    plt.title("Count time series")
    plt.plot(data_pd['count'], c = "r", marker = 'o', ls = '--')
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.savefig('test.png') #그림 저장
    plt.show()

    return sum(data_pd['count'])

sm = 0
n = 0

path = "C:\\Users\\1\\Desktop\\dis\\postick.csv"
tmp = printSummary(path)

sm += tmp
n += 1

print("현재까지 검색어량 평균:", sm / n)