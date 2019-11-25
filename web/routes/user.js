// google trends json object 받아오기
const googleTrends = require('../node_modules/google-trends-api/lib/google-trends-api.min.js');
const async = require('async');

var loadFirstPage = function(req, res) {
    console.log('/ 패스 요청됨.');
    res.render('index.ejs');
};

var showResults = function(req, res) {
    console.log('/showResults 패스 요청됨.');
    var keyword = req.param('keyword');
    var startDate = req.param('startDate');
    var endDate = req.param('endDate');

    console.log('/showResults 사용자가 입력한 검색어는 ' + keyword);
    console.log('/showResults 사용자가 입력한 날짜 ' + startDate + ' ' + endDate);
    data_Processing([keyword, startDate, endDate], "searchResult.ejs", req, res);
};


var compareKeywords = function(req, res) {
    console.log('/compareKeywords 패스 요청됨.');
    var compare = req.param('compare');
    
    console.log('/compareKeywords 사용자가 입력한 비교 검색어는 ' + compare);
    data_Processing([compare], "keywordCompare.ejs", req, res); //날짜는 빠진 상태

};

function FindRecentMonth() {
    var lastDay = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    var date = new Date();
    var str;

    var trailMonth = (date.getMonth() + 11) % 12;
    var year = date.getFullYear();

    if (trailMonth == 11)
        year--;

    if (year % 400 == 0 || ( year % 4 == 0 && year % 100 != 0))
            lastDay[1]++;

    str = year + "-" + (trailMonth + 1) + "-" + lastDay[trailMonth];

    return str;
}

function oneYearsAgo() {
    var date = new Date();
    var str;

    date.setFullYear(date.getFullYear() - 1);

    str = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();

    return str 
}



function check_params (params)
{
    if(params[1] == undefined ) //startDate
    {
        params[1] = oneYearsAgo();      
    }
    
    if(params[2] == undefined ) //endDate
    {
        params[2] = FindRecentMonth();      
    }
    
    return params;
}

function data_Processing(params, ejsFileName, req, res) {
    var args = check_params(params);
    var answerPermissions = new AnswerPermissions(args[0], args[1], args[2]);   
    
    /* 병렬 처리 */
    async.parallel([
        answerPermissions.get_gTrend_graphData, /* 병렬로 실행 시킬 함수 리스트, 현재 3개 */
        answerPermissions.get_gTrend_related_Data,
        answerPermissions.get_nTrend_crawling_Data /* naver */
      ],
      function(err, results) { /* 각 함수 마다 return 값들이 results 배열로 들어가 있음 */
        if (err) {
          console.log(err);
        }
        /* if sucess */
        google = {
                'graphData': results[0],
                'related': results[1]
        };

        var DataSet = {};
        DataSet['google'] = google;
        DataSet['naver'] = results[2];
        string = JSON.stringify(DataSet);
        DataSet["JSONString"] = string;
        console.log(DataSet);

        var context = { keyword: args[0], dataSet: DataSet }
        req.app.render(ejsFileName, context, function(err, html) {
            if (err) {
                console.error('뷰 렌더링 중 에러 발생 : ' + err.stack);
                return;
            }
            res.end(html);
        });
    });
}


/* Node.js Async.series functions 에게 매개 변수를 넘기기 위해 Using a object style */
var AnswerPermissions = function(keyword, startDate, endDate) {

 /* attribute, 넘길 매개 변수들을 저장 */
  this.keyword = keyword;
  this.startDate = startDate;
  this.endDate = endDate;
    
 /* method  */
  this.get_gTrend_graphData = function(callback) {
        return new Promise(function(resolve, reject) {

        googleTrends.interestOverTime({
                keyword: keyword,
                startTime: new Date(startDate),
                endTime: new Date(endDate),
                granularTimeResolution: true,
            })
            .then(function(results) {
                var googlePeriod = [];
                var googleCount = [];
                trendobj = JSON.parse(results);

                for (var i = 0; i < trendobj['default']['timelineData'].length; i++) {
                    var changedDate;
                    changedDate = new Date(trendobj['default']['timelineData'][i]['formattedAxisTime']);
                    changedDate = changedDate.toISOString().substring(0, 10).toString();
                    // console.log(changedDate);
                    googlePeriod.push(changedDate);
                    googleCount.push(trendobj['default']['timelineData'][i]['value'][0]);
                }

                google = {
                    'period': googlePeriod,
                    'count': googleCount
                };
                //resolve(google);
                callback(null, google); /* callback : google을 return 해주는 역할 */
            })

    })
  };
 
  this.get_gTrend_related_Data = function(callback) {
     return new Promise(function(resolve, reject) {

        googleTrends.relatedQueries({
                keyword: keyword,
                startTime: new Date(startDate),
                endTime: new Date(endDate),
                granularTimeResolution: true,
            })
            .then((res) => {
                trendobj = JSON.parse(res);

                var top = trendobj['default']['rankedList'][0]['rankedKeyword']; // query랑 value만 얻어오면 됨 (sorting 되어 있음)
                var rising = trendobj['default']['rankedList'][1]['rankedKeyword']; // query value(단위 %) (breakout이면 급상승), 그 외는 수치 

                var googleTop_related = [];
                var googleTop_rate = [];
                var googleRising_related = [];
                var googleRising_rate = [];

                for (var i = 0; i < top.length; i++) {
                    googleTop_related.push(top[i].query);
                    googleTop_rate.push(top[i].value);
                }

                for (var i = 0; i < rising.length; i++) {
                    googleRising_related.push(rising[i].query);
                    googleRising_rate.push(rising[i].value);
                }



                top = {
                    'relatedKeyword': googleTop_related,
                    'rate': googleTop_rate
                };

                rising = {
                    'relatedKeyword': googleRising_related,
                    'rate': googleRising_rate
                };

                related = {
                    'top': top,
                    'rising': rising
                };

                callback(null, related);

            })
            .catch((err) => {
                console.log(err);
            })

    })
  };
/* 파이썬으로 실행한 코드
  this.get_nTrend_crawling_Data = function(callback) {
        return new Promise(function(resolve, reject) {

    let { PythonShell } = require('python-shell')

    var options = {
        mode: 'text',
        pythonPath: './venv/bin/python',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: [keyword, startDate, endDate]
    };

    PythonShell.run('data_processing.py', options, function(err, results) {
        if (err) throw err;

        if (results[0] == '성공') {
            var obj = JSON.parse(results[1]); // JSON object
            //console.log(obj)
            //console.log(obj.naver.graphData) // 이게 그 기존의 배열

            var NaverPeriod = [];
            var NaverCount = [];

            for (var i = 0; i < obj.naver.graphData.length; i++) {
                NaverPeriod.push(obj.naver.graphData[i][0]);
                NaverCount.push(obj.naver.graphData[i][2]);
            }


            obj.naver.graphData = {
                'period': NaverPeriod,
                'count': NaverCount
            }

            //string = JSON.stringify(obj);
            //obj["JSONString"] = string;
            //obj["keyword"] = keyword;

            callback(null, obj);
            
        }
    });

    })
  };
*/


this.get_nTrend_crawling_Data = function(callback) {
        new Promise(function(resolve, reject) {
            // nodejs 크롤링을 위한 모듈
            const puppeteer = require('puppeteer');
            (async () => {
                const browser = await puppeteer.launch();
                const page = await browser.newPage();
                //키워드값 넣는곳
                //const keyword = keyword;
                //해당 사이트로 간다
                await page.goto('http://surffing.net/');
                //입력상자에 값넣기
                await page.evaluate((id) => {
                    document.querySelector('#saerchKeyword').value = id;
                    // document.querySelector('#pw').value = pw;
                }, keyword);
                //검색버튼 클릭
                await page.click('.key-btn');
                //약 2초 동안 대기함, 시간줄이면 잘 안됨
                await page.waitFor(2000);
                //밑에 페이지 변동됐을때 해당리스트에서 값 뽑아옴
                const element1 = await page.evaluate(() => {
                    const anchors = Array.from(document.querySelectorAll('td'));
                    return anchors.map(anchor => anchor.textContent); //각 원소마다 textContent, 즉 문자값을 받아옴
                });
                //값에 \t와 \n이 들어가있는 경우가 있어서 그것을 대체해주는 함수
                String.prototype.replaceAll = function(org, dest) {
                    return this.split(org).join(dest);
                }
                //원소별로 replaceall 해줌
                for (var i = 0; i < element1.length; i++) {
                    element1[i] = element1[i].replaceAll('\t', '').replaceAll('\n', '');
                }
                // 원소 배열들에게 나누기
                relatedKeywords = {} //연관 검색어 : [pc, mobile]
                publishVolumes = {} // blog : 발행량, cafe : 발행량, knwlgin : 발행량
                var count = 0;
                for (var i = 0; i < 3; i++) {
                    count += 1;
                    if (count % 3 == 1) //월간 블로그 발행량
                        publishVolumes['blog'] = element1[i];
                    else if (count % 3 == 2) //월간 카페 발행량
                        publishVolumes['cafe'] = element1[i];
                    else //월간지식인 발행량
                        publishVolumes['knwlgin'] = element1[i];
                }
                // 연관검색어들의 정보를 담을 애들
                var bufferKey = "";
                var bufferPC = "";
                var bufferM = "";
                count = 0;
                for (i = 6; i < element1.length; i++) {
                    count += 1

                    if (count % 3 == 1) // 연관 검색어
                        bufferKey = element1[i]
                    else if (count % 3 == 2) // 월간 검색수 PC
                        bufferPC = element1[i]
                    else //월간 검색수 모바일
                        bufferM = element1[i]

                    relatedKeywords[bufferKey] = [bufferPC, bufferM]
                }
                //console.log(publishVolumes);
                //console.log(relatedKeywords);


                //screenshot찍어서 나옴, 테스트용, 지워도됨
                //await page.screenshot({ path: 'surffing.png', fullPage: true });
                //browser 종료, 지우면 안됨
                await browser.close();
                resolve(relatedKeywords);
            })();
        }).then(function(crawling_result) { //크롤링 값 받았으니까 
            //console.log(crawling_result); 

            /* moudules */
            var request = require('request');
            var moment = require('moment');

            moment().format("YYYY-MM-DD");
            var nowDate = moment(new Date(moment().year(), moment().month(), moment().date()));

            // --------------------------------- 여기에 최근 1달 값 크롤링한게 들어가야합니다 -----------
            var first_value = crawling_result[Object.keys(crawling_result)[0]];
            var count = [];
            for (var j in first_value) {
                var str = "";
                var test = first_value[j].split(",")
                for (var i in test) {
                    str += test[i];
                }
                count[j] = Number(str)
            }

            var searchword_specific = [count[0], count[1], count[0] + count[1]];

            // related == 기존의 연관검색어 : [pc, mobile] 쌍
            var related = crawling_result;
            for (var i in related) {
                for (var j in related[i]) {
                    // 10 미만에 대한 처리 => 0으로 만듬
                    var token;
                    if (related[i][j] === '10 미만') {
                        related[i][j] = 0;
                    }
                    // 10 미만이 아닌 경우 ','로 토큰만들어서 넘버로 전환
                    else {
                        token = related[i][j].split(',');
                        var str = "";
                        for (var k in token) {
                            str += token[k];
                        }
                        related[i][j] = Number(str);
                    }
                }
                // 세 번째 인덱스에 pc, mobile의 합계를 넣음
                related[i][2] = related[i][0] + related[i][1];
            }

            // key => key들의 list와 리스트별 인덱싱을 하기위한 keyvalue만들기위해 임시로 사용
            key = [];
            // keylist => 연관검색어를 array 형식으로 임시보관하는 용도
            keylist = [];
            // keyvalue => 기존 related에 서로 다른 킷값으로 저장되어있어서
            // 1차적으로 서로 다른 킷값에 대한 전체 검색량을 보관하기 위한 용도
            // 2차적으로 전체 검색량에 대해 내림차순 정렬 시 몇 번째 인덱스인지 표시하는 용도
            keyvalue = [];
            // keylist와 keyvalue의 초기화 for문
            for (key in related) {
                keylist.push(key);
                keyvalue.push([related[key][2], 0]);
                // keyvalue.push([0, 0]);
            }

            // keyvalue = [[전체검색량, 들어갈 index], [.. , ..], .. ]로
            // 나중에 넣을 index 구할 2중 for문
            for (var i in keyvalue) {
                for (var j in keyvalue) {
                    // 현재 index 구할 것보다 더 작은 값이 존재한다면
                    // 내림차순시 index가 1 증가해야함
                    if (keyvalue[i][0] < keyvalue[j][0]) {
                        keyvalue[i][1] += 1;
                    }
                    // 현재 index 구할 것과 같다면 한쪽은 +1을 해줘야 중복이 발생하지 않음
                    if (keyvalue[i][0] == keyvalue[j][0] && i < j) {
                        keyvalue[i][1] += 1;
                    }
                }
            }

            // sortedRelated => 최종적으로 정렬해서 내보낼 related = {}
            var sortedRelated = {};
            // keylist, keyvalue로 했지만 i, j 범위 이상의 의미는 없음
            // sortedRelated에 아까 구한 keyvalue의 들어갈 index별로
            // 연관검색어 : [pc, mobile, total]을 집어넣는 for문
            for (i in keylist) {
                index = 0;
                for (j in keyvalue) {
                    // i == 0일때 예시로 들면
                    // keyvalue[j][1] == 0이면
                    // (keylist[j] 에 들어있는 연관검색어) :
                    // (related[연관검색어]에 들어있는 [pc, mobile, total])을
                    // sorted에 넣는다는 의미
                    if (keyvalue[j][1] == i) {
                        index = j;
                    }
                }
                // console.log(keylist[index]);
                // console.log(keyvalue[index][1]);
                sortedRelated[keylist[index]] = related[keylist[index]];
            }
            //console.log(sortedRelated);


            var defined = count[0] + count[1]; //절대 값
            // --------------------------------- 여기에 최근 1달 값 크롤링한게 들어가야합니다 -----------

            /* naver-trend-api parameters */
            var client_id = 'QqTTJVe3ttjxiFKxy6gi';
            var client_secret = 'GqJHHxrHRX';
            var api_url = 'https://openapi.naver.com/v1/datalab/search';
            var request_body = {
                "startDate": startDate,
                "endDate": endDate,
                "timeUnit": "month",
                "keywordGroups": [{
                    "groupName": " ",
                    "keywords": [
                        "치킨"
                    ]
                }],
                "device": "pc",
                "ages": [
                    "1",
                    "2"
                ],
                "gender": "f"
            };

            // returndata가 원래 csv로 저장시키던거
            var returndata = {};


            request.post({
                    url: api_url,
                    body: JSON.stringify(request_body),
                    headers: {
                        'X-Naver-Client-Id': client_id,
                        'X-Naver-Client-Secret': client_secret,
                        'Content-Type': 'application/json'
                    }
                },
                function(error, response, body) {
                    dataset = JSON.parse(body).results[0].data;
                    length = Object.keys(dataset).length;
                    recentRatio = dataset[length - 1].ratio;

                    graphData = {};
                    //data = [];
                    var NaverPeriod = [];
                    var NaverCount = [];

                    for (var i = 0; i < length; i++) {
                        if (moment(endDate).diff(moment(dataset[i].period), "months") < 1) {
                            break;
                        }
                        //var temp = [dataset[i].period, dataset[i].ratio, dataset[i].ratio * defined / recentRatio];
                        //data[i] = temp;
                        NaverPeriod.push(dataset[i].period);
                        NaverCount.push(dataset[i].ratio * defined / recentRatio);
                    }

                    data = {
                        'period': NaverPeriod,
                        'count': NaverCount
                    };



                    var naver = {
                        'graphData': data,
                        'searchword': searchword_specific,
                        // 'related': related
                        'related': sortedRelated
                    };

                    //console.log(naver);
                    //return naver;
                    callback(null, naver);

                });
        });
    };

 };




module.exports.loadFirstPage = loadFirstPage;
module.exports.showResults = showResults;
module.exports.compareKeywords = compareKeywords;
//module.exports.doho = doho;