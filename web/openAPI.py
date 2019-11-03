import json
import urllib.request

# naver Open API
# 주어진 구간에 대한 검색함수. json -> dict -> list 형식으로 변환하여 재구성해서 반환
def naverAPI_section_search(StartDate, EndDate, Keyword, DeviceType):

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