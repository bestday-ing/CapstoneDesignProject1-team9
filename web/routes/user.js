var loadFirstPage = function(req, res) {
	console.log('/ 패스 요청됨.');
	res.render('index.ejs');
};

var showResults = function(req, res) {
    console.log('/showResults 패스 요청됨.');
    var keyword = req.param('keyword');
    console.log('/showResults 사용자가 입력한 검색어는 ' + keyword);
    // 받은 키워드로 여러가지 연산 처리한 후 데이터 셋에 담았다고 가정 -- 나중에 채울 것임
    var dataSet = [];
    //res.writeHead('200', { 'Content-Type': 'text/html;charset=utf8' });
    var context = { keyword: keyword, dataSet : dataSet };
    req.app.render("searchResult.ejs", context, function(err, html) {
        if (err) {
            console.error('뷰 렌더링 중 에러 발생 : ' + err.stack);
            return;
        }
        res.end(html);
    });

};

module.exports.loadFirstPage = loadFirstPage;
module.exports.showResults = showResults;