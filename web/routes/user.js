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
    console.log('/showResults 사용자가 입력한 날짜 ' + startDate + ' ' + endDate );
    data_Processing( [keyword, startDate, endDate] , "searchResult.ejs", req, res);
};


var compareKeywords = function(req, res) {
    console.log('/compareKeywords 패스 요청됨.');
    var compare = req.param('compare');
    
    console.log('/compareKeywords 사용자가 입력한 비교 검색어는 ' + compare);
    data_Processing( [compare] , "keywordCompare.ejs", req, res );

};

function data_Processing( args , ejsFileName, req, res ){
    
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
        
    if(results[0]=='성공'){
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
            'period' : NaverPeriod,
            'count' : NaverCount
        }
        
        
        string = JSON.stringify(obj);
        obj["JSONString"] = string;
        //obj["keyword"] = keyword;
        console.log(obj);

       var context = { keyword: args[0], dataSet : obj };
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

module.exports.loadFirstPage = loadFirstPage;
module.exports.showResults = showResults;
module.exports.compareKeywords = compareKeywords;