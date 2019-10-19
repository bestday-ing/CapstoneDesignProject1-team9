
            //var temp;
            // function input(){
            //     var input = document.getElementById("keyword-formbuilder-2").value;
            //     temp = input;
            //     // temp = openSomehowPythonInterpreter("./Crawler.py", "get_abs_value_naver(temp)");
            // }

            // function output(){
            //     document.getElementById("output").value = temp;
            // }    


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
