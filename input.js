
            var temp;
            function input(){
                var input = document.getElementById("keyword-formbuilder-2").value;
                temp = input;
                // temp = openSomehowPythonInterpreter("./Crawler.py", "get_abs_value_naver(temp)");
            }

            function output(){
                document.getElementById("output").value = temp;
            }    


            var spawn = require('child_process').spawn,
            py = spawn('python',['Crawler.py']),
            jsonObject = new Object();
            jsonObject.keyword = "삼성";

            dataString = ''
            py.stdout.on('data',function(data){
                    dataString +=data.toString();
            });
            py.stdout.on('end',function(){
                console.log('Sum of numbers=',dataString);

            });
            py.stdin.write(JSON.stringify(jsonObject));
            //py.stdin.write("삼성");
            
            py.stdin.end();

            
//             $.ajax({
//               type: "POST",
//               url: "./Crawler.py",
//               data: { param: temp}
//           }).done(function( o ) {
//    // do something
// });
