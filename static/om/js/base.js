// editor:bruce
// time:2016-9-5

function test(){
	alert('this is a test javascript fuction');
};

// //加载服务器组信息
// function loadOMgroupinfo(){
// 	// document.getElementById("servergroup").options.length=0;
// 	var url ='/OM/LoadGroupInfo/';
// 	var myAjax = new Ajax.Request(
// 		url,
// 		{
// 			method:'get',
// 			onComplete:showResponse
// 		});
// 	function showResponse(originalRequest){
// 		var html = originalRequest.responseText;
// 		var objarray = html.split(";");
// 		for ( var i=0;i<html.split(";").length-1;i++){
// 			var oOption = document.createElement('OPTION');
// 			oOption.value = objarray[i].split(',')[0];//id
// 			oOption.text = oOption.value+'|'+objarray[i].split(',')[1];//内容,实际显示部分
// 			document.servergroupForm.servergroup.options.add(oOption);
// 		}
// 	}
// };

// //加载服务器列表信息
// function loadOMuserinfo(){
// 	var url ='/OM/LoadOMUserInfo/';
// 	var myAjax = new Ajax.Request(
// 		url,
// 		{
// 			method:'get',
// 			onComplete:showResponse
// 		});
// 	function showResponse(originalRequest){
// 		// alert('1')
// 		// alert(originalRequest.responseText);
// 		// console.log(originalRequest.responseText)
// 		var html = originalRequest.responseText;
// 		var objarray = html.split(";");
// 		// alert('2')
// 		// var options_value = objarray.split(',')[0];
// 		// var options_text = objarray.split(',')[1];
// 		// alert('3')
// 		for ( var i=0;i<html.split(";").length-1;i++){
// 			var oOption = document.createElement('OPTION');
// 			oOption.value = objarray[i].split(',')[0];//name
// 			oOption.text = oOption.value+'|'+objarray[i].split(',')[1];//ip,实际显示部分
// 			document.serveruserForm.serveruser.options.add(oOption);
// 		}
// 	}

// };



function userchange(ths){
	console.log(ths.value)
};

// function showSelectitems(ths){
// 	// var itmes = ths
// 	// var aa = itmes.split()
// 	var itmes = document.getElementById(ths).innerHTML
// 	console.log(itmes)
// }

function om_group_mod(ths){
	var aa = ths.getAttribute("value");
	// alert(aa)
	// alert('om_group_add')
	if(aa=='add'){
		// bb = document.getElementById('addTable')
		// bb.style.display= "block"

		var url ='/OM/test/';
		var myAjax = new Ajax.Request(
			url,
			{
				method:'get',
				onComplete:showResponse
			});
		function showResponse(originalRequest){
			// alert('1')
			alert(originalRequest.responseText);
			// console.log(originalRequest.responseText)
			var html = originalRequest.responseText;
			var objarray = html.split(";");
			alert('2')
			// var options_value = objarray.split(',')[0];
			// var options_text = objarray.split(',')[1];
			alert('3')
			for ( var i=0;i<html.split(";").length-1;i++){
				var oOption = document.createElement('OPTION');
				oOption.value = objarray[i].split(',')[0];
				oOption.text = objarray[i].split(',')[1];
				document.systemForm.servergroup.options.add(oOption);
				// alert(options_value)
			}
			// var oOption = document.createElement('OPTION')
			// alert('2')
			// oOption.value = html
			// alert('3')
			// oOption.text = '加载中'
			// alert('4')

			// document.systemForm.servergroup.options.add(oOption);
			// alert('5')
			// alert(html);
			// document.getElementById('test').innerHTML=html;
			// alert('this is a test javascript fuction');
		}
		//弹窗增加用户组界面
		alert('增加界面')
	}else{
		//弹窗删减界面
		alert('删除界面')

	}
};