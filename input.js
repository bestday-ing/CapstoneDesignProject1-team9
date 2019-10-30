
            //var temp;
            // function input(){
            //     var input = document.getElementById("keyword-formbuilder-2").value;
            //     temp = input;
            //     // temp = openSomehowPythonInterpreter("./Crawler.py", "get_abs_value_naver(temp)");
            // }

            // function output(){
            //     document.getElementById("output").value = temp;
            // }    

/*
            var spawn = require('child_process').spawn,
            py = spawn('python',['Edited_TEAM_9_naverSearchAPI.py']),
            jsonObject = new Object();
            jsonObject.keyword = "samsung";
            jsonObject.test = "test";

            dataString = '';
            py.stdout.on('data',function(data){
                    dataString +=data.toString();
            });
            py.stdout.on('end',function(){
                console.log('Read STring=',dataString);
            });
            py.stdin.write(JSON.stringify(jsonObject));
            //py.stdin.write("삼성");
            
            py.stdin.end();
            console.log(py.stdout.read(2048));
*/

let { PythonShell } = require('python-shell')

var options = {
    mode: 'text',
    pythonPath: './venv/bin/python',
    pythonOptions: ['-u'],
    scriptPath: '',
    args: ['삼성']
};


PythonShell.run('Edited_TEAM_9_naverSearchAPI.py', options, function(err, results) {
    if (err) throw err;
    //results[0] : "['test.py', 'value1', 'value2', 'value3', 'a', 'b', 'c']" 인 상태
    var str = results[0]
      str = str.replace(/'/g, '"'); // '' 를 " "로 바꿈
      array = JSON.parse(str)
      console.log('typeof:', typeof(array));
      console.log(array);
      console.log(array[0]); //원소 하나 뽑기
});


