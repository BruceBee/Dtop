// time:2016-09-22
// author:bruce

function downData(){
	var inputChecks=$("input:checkbox[name='dataFrom_check']:checked");
	if(inputChecks.length==0){
		layer.alert('请选中导出项！');
		return;
	}
	var dbname =$("#downData").attr("name")
	// alert(dbname)
	// alert(dbname)
	// var orders='';
	// for(var i=0;i<inputChecks.length;i++){
	// 	orders+=inputChecks[i].value;
	// 	if(i!=inputChecks.length-1){
	// 		orders+=',';
	// 	}
	// }


	$.ajax({
		type:'POST',
		url:'/BulidData/',
		dataType:'text',
		data:{'dbname':dbname},
		success:function(text){
			// console.log(text)
			var url ='/download/'+text;
			window.location.href=url;
			// layer.alert('导入成功')
		},error:function(){
			layer.alert('导入失败');
		}
	});
	
}