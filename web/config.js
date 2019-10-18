/*
 * 설정 파일
 *
 * @date 2016-11-10
 * @author Mike
 */

module.exports = {
	server_port: 3000,
	//db_url: 'mongodb://localhost:27017/local',
	//db_schemas: [
	//    {file:'./user_schema', collection:'users3', schemaName:'UserSchema', modelName:'UserModel'}
	//],
	route_info: [
	    //===== User =====//
	    {file:'./user', path:'/', method:'loadFirstPage', type:'get'}, //user.loadFirstPage
        {file:'./user', path:'/showResults', method:'showResults', type:'get'} //user.showResults
	]
}