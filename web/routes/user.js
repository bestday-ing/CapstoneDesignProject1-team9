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
    data_Processing([compare], "keywordCompare.ejs", req, res);

};

function data_Processing(args, ejsFileName, req, res) {

    let { PythonShell } = require('python-shell')

    var options = {
        mode: 'text',
        pythonPath: './venv/bin/python',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: args
    };

    PythonShell.run('data_processing.py', options, function(err, results) {
        if (err) throw err;

        if (results[0] == '성공') {
            console.log()
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


            string = JSON.stringify(obj);
            obj["JSONString"] = string;
            //obj["keyword"] = keyword;
            console.log(obj);

            var context = { keyword: args[0], dataSet: obj };
            req.app.render(ejsFileName, context, function(err, html) {
                if (err) {
                    console.error('뷰 렌더링 중 에러 발생 : ' + err.stack);
                    return;
                }
                res.end(html);
            });
        }
    });
}


var doho = function(req, res) {
    console.log('/doho 패스 요청됨.');
    var reqkeyword = req.param('keyword');
    var startDate = req.param('startDate');
    var endDate = req.param('endDate');

    console.log('/doho 사용자가 입력한 검색어는 ' + reqkeyword);
    console.log('/doho 사용자가 입력한 날짜 ' + startDate + ' ' + endDate);



    // google trends json object 받아오기
    var googleTrends = require('../node_modules/google-trends-api/lib/google-trends-api.min.js');
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
                console.log(changedDate);
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

module.exports.loadFirstPage = loadFirstPage;
module.exports.showResults = showResults;
module.exports.compareKeywords = compareKeywords;
module.exports.doho = doho;