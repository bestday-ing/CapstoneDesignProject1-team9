var loadFirstPage = function(req, res) {
    console.log('/ 패스 요청됨.');
    res.render('index.ejs');
};

var showResults = function(req, res) {
    console.log('/showResults 패스 요청됨.');
    var keyword = req.param('keyword');
    console.log('/showResults 사용자가 입력한 검색어는 ' + keyword);
    // 받은 키워드로 여러가지 연산 처리한 후 데이터 셋에 담았다고 가정 -- 나중에 채울 것임

    let { PythonShell } = require('python-shell')

    var options = {
        mode: 'text',
        pythonPath: './venv/bin/python',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: [keyword]
    };

    // naver API 
    PythonShell.run('Edited_TEAM_9_naverSearchAPI.py', options, function(err, results) {
        if (err) throw err;
        //results[0] : "['test.py', 'value1', 'value2', 'value3', 'a', 'b', 'c']" 인 상태
        var str = results[0]
        str = str.replace(/'/g, '"'); // '' 를 " "로 바꿈
        var dataSet = JSON.parse(str)
        // console.log('typeof:', typeof(array));
        console.log(dataSet);

        /* dataSet test*/
        //console.log(dataSet[0]); //원소 하나 뽑기
        console.log(typeof(dataSet[0][0]));
        //console.log(dataSet.length);

        var period = [];
        var count = [];

        for (var i = 0; i < dataSet.length; i++) {
            period.push(dataSet[i][0]);
            count.push(dataSet[i][2]);
        }
        
        console.log(period);
        console.log(count);

        // naver : json 객체 , daum : json 객체 이런 식으로 나중에 구상해야지
        //var obj = { period: dataSet[0], count: dataSet[2] };
        //var myJSON = JSON.stringify(obj);
        //console.log(myJSON);

        var context = { keyword: keyword, period: period, count: count };
        req.app.render("searchResult.ejs", context, function(err, html) {
            if (err) {
                console.error('뷰 렌더링 중 에러 발생 : ' + err.stack);
                return;
            }
            res.end(html);
        });
    });



};

module.exports.loadFirstPage = loadFirstPage;
module.exports.showResults = showResults;