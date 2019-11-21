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

function data_Processing(args, ejsFileName, req, res) {
    var answerPermissions = new AnswerPermissions(args[0], "2016-01-01", "2018-12-31");  //날짜 나중에 undefined 처리해서 여기만 바꿔주면 되겠다. 시작 날짜와 종료 날짜는 args[1] args[2] 에 들어 있음. 
    
    /* 병렬 처리 */
    async.parallel([
        answerPermissions.get_gTrend_graphData, /* 병렬로 실행 시킬 함수 리스트, 현재 3개 */
        answerPermissions.get_gTrend_related_Data,
        answerPermissions.get_nTrend_crawling_Data
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

        results[2]['google'] = google;
        string = JSON.stringify(results[2]);
        results[2]["JSONString"] = string;
        console.log(results[2]);

        var context = { keyword: args[0], dataSet: results[2] }
        req.app.render(ejsFileName, context, function(err, html) {
            if (err) {
                console.error('뷰 렌더링 중 에러 발생 : ' + err.stack);
                return;
            }
            res.end(html);
        });
    });
}


/* Node.js Async.series functions 에게 매개 변수를 넘기기 위해 Using a object 한 것, 나중에 다른 파일로 모듈화시킬 예정 */
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
                var rising = trendobj['default']['rankedList'][1]['rankedKeyword']; // query formattedValue (breakout이면 급상승), 그 외는 수치 
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
                    googleRising_rate.push(rising[i].formattedValue);
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


 };



/* google-trend-api test 용 -- success, thank u doho developer
var doho = function(req, res) {
    console.log('/doho 패스 요청됨.');
    var reqkeyword = req.param('keyword');
    var startDate = req.param('startDate');
    var endDate = req.param('endDate');

    console.log('/doho 사용자가 입력한 검색어는 ' + reqkeyword);
    console.log('/doho 사용자가 입력한 날짜 ' + startDate + ' ' + endDate);


    // const fs = require('fs');
    var dohoobj = new Object();
    var googlePeriod = [];
    var googleCount = [];
    let trendobj;

    googleTrends.interestOverTime({
        keyword: reqkeyword,
        startTime: new Date(startDate),
        endTime: new Date(endDate),
        granularTimeResolution: true,
    }, function(err, results) {
        if (err) console.log('oh no error!', err);
        // else console.log(JSON.parse(results).value);
        else {
            trendobj = JSON.parse(results);
            // for (var i = 0; i < 10; i++)
            //     console.log(obj['default']['timelineData'][i]); 
            for (var i = 0; i < trendobj['default']['timelineData'].length; i++) {
                var changedDate;
                changedDate = new Date(trendobj['default']['timelineData'][i]['formattedAxisTime']);
                changedDate = changedDate.toISOString().substring(0,10).toString();
                // console.log(changedDate);
                googlePeriod.push(changedDate);
                googleCount.push(trendobj['default']['timelineData'][i]['value'][0]);
            }


            
            // fs.writeFileSync('test.json', results, 'utf-8');
            //console.log(googlePeriod);
            //console.log(googleCount);
            dohoobj = {
                'period': googlePeriod,
                'count': googleCount
            };
            
            data_Processing([reqkeyword, startDate, endDate], "searchResult.ejs", dohoobj, req, res);

            var context = { keyword: reqkeyword, dataSet: dohoobj };
            req.app.render("doho.ejs", context, function(err, html) {
                if (err) {
                    console.error('뷰 렌더링 중 에러 발생 : ' + err.stack);
                    return;
                }
                res.end(html);
            }); 
        }
    });

}
*/



module.exports.loadFirstPage = loadFirstPage;
module.exports.showResults = showResults;
module.exports.compareKeywords = compareKeywords;
//module.exports.doho = doho;