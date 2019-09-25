from rpy2.robjects import r
from matplotlib import pyplot as plt
import pandas as pd

from naverSearchAPI import Search

def printSummary(path):
    r.assign('path', path)
    r('data <- read.csv(path, header = T)')
    r('print(summary(data[,2:4]))')
    # 0, 70, 611, 291 뷰 사이즈 만큼 그림 사이즈 줄이기

    data = pd.read_csv(path)

    feature = ['Period', 'ratio', 'count']

    data_pd = data[feature]

    plt.title("Count time series")
    plt.plot(data_pd['count'], c = "r", marker = 'o', ls = '--')
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.savefig('result.png') #그림 저장
    # plt.show()

    return sum(data_pd['count'])





