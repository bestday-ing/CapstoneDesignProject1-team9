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
    
    // 받은 키워드로 여러가지 연산 처리한 후 데이터 셋에 담았다고 가정 -- 나중에 채울 것임

    let { PythonShell } = require('python-shell')

    var options = {
        mode: 'text',
        pythonPath: './venv/bin/python',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: [keyword]
    };

    PythonShell.run('thread_crawling.py', options, function(err, results) {
    if (err) throw err;
    //results[0] : "['test.py', 'value1', 'value2', 'value3', 'a', 'b', 'c']"
    if(results[0]=='성공'){
        console.log()
        var obj = JSON.parse(results[1]);
        console.log(obj)
        //console.log(obj.naver.graphData) //이게 그 기존의 배열

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

        console.log(obj.naver) //이게 그 기존의 배열

        var context = { keyword: keyword, dataSet : obj };
        req.app.render("searchResult.ejs", context, function(err, html) {
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