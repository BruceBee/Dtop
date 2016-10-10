$.fn.dataTable = function(obj) {     
      var json = $.extend({
				title:'',//标题
				columns:[],//列
				formid:'',
				loadAfter:null
			}, obj);
	//开始熏染标签<div>
	var div=$(this);
	div.empty();
	//开始生成tab容器标签
	var boxDiv=$("<div></div>").addClass("widget-box");
	//生成标题
	var titleDiv=$("<div class='widget-title'><span class='icon'><i class='icon-th'></i></span><h5>"+json.title+"</h5></div>");
	boxDiv.append(titleDiv);
	div.append(boxDiv);
	
	//生成表格头部
	var tabDiv=$("<div class='widget-content nopadding'></div>");
	var table=$("<table class='table table-bordered data-table dataTable' id='"+json.formid+"_table'></table>");
	var thead=$("<thead></thead>");
	var trhead=$("<tr></tr>");
		trhead.attr("role","row");
	tabDiv.append(table);
	table.append(thead);
	thead.append(trhead);
	for(var i=0;i<json.columns.length;i++){
		var th=$("<th class='ui-state-default'></th>");
		if(json.columns[i].width){
			th.css("width",json.columns[i].width);
		}
		var trDiv=$("<div class='DataTables_sort_wrapper'></div>");
		if(json.columns[i].check){
			var inputCheck=$("<input type='checkbox' id='"+json.formid+"_checkAll'/>");
			trDiv.append(inputCheck);
			if(json.columns[i].checkAll){
				inputCheck.on("click",function(){
					var checkState=this.checked;
					$("input[name='"+json.formid+"_check']").each(function(){
						this.checked=checkState;
					});
				});
			}
		}else{
			trDiv.html(json.columns[i].name);
		}
		trhead.append(th);
		th.append(trDiv);
	}
	boxDiv.append(tabDiv);
	if(json.formid==''){
		return;
	}
	var tbody=$("<tbody role='alert' aria-live='polite' aria-relevant='all'></tbody>");
	var toolbar=$("<div class='fg-toolbar ui-toolbar ui-widget-header ui-corner-bl ui-corner-br ui-helper-clearfix' style='border-bottom: 1px solid #CDCDCD;'></div>");
	var successFunction=function(jsonData){
		tbody.empty();
		toolbar.empty();
		if(jsonData.rows&&jsonData.rows.length!=0){
			for(var q=0;q<jsonData.rows.length;q++){
				var atr=$("<tr class='gradeA odd'></tr>");
				for(var i=0;i<json.columns.length;i++){
					var key=json.columns[i].key;
					var atd=$("<td></td>");
					if(json.columns[i].check){
						var tdInputCheck=$("<input type='checkbox' name='"+json.formid+"_check' id='"+json.formid+"_check_"+jsonData.rows[q][key]+"' value='"+jsonData.rows[q][key]+"'/>");
						atd.append(tdInputCheck);
						if(!json.columns[i].checkAll){
							tdInputCheck.on('click',function(){
								var checkState=this.checked;
								if(checkState){
									$("input[name='"+json.formid+"_check']").each(function(){
										this.checked=false;
									});
									this.checked=checkState;
								}
							});					
						}
					}else{
						atd.html(jsonData.rows[q][key]);
					}
					
					if(json.columns[i].align){
						atd.css("text-align",json.columns[i].align);
					}

					if(json.columns[i].valign){
						atd.css("vertical-align",json.columns[i].valign);
					}

					atr.append(atd);
				}
				tbody.append(atr);
			}
			table.append(tbody);
		}
		var nowPage=$("#"+json.formid).find("input[name='page']");
		//显示页码  
		
		boxDiv.append(toolbar);
		var paginate=$("<div class='dataTables_paginate fg-buttonset ui-buttonset fg-buttonset-multi ui-buttonset-multi paging_full_numbers' id='DataTables_Table_0_paginate' style='padding-bottom:5px;'></div>");
			toolbar.append(paginate);
		
		var first=$("<a tabindex='0' class='first ui-corner-tl ui-corner-bl fg-button ui-button ui-state-default' id='"+div.attr("id")+"_first'>第一页</a>");
		var previous=$("<a tabindex='0' class='previous fg-button ui-button ui-state-default' id='"+div.attr("id")+"_previous'>上一页</a>");
		if(nowPage.val()=='1'){
			first.addClass("ui-state-disabled");
			previous.addClass("ui-state-disabled");
		}
		paginate.append(first);
		paginate.append(previous);
		
		//显示页码
		var length=0;
		var showNum=$("#"+json.formid).find("input[name='num']").val()|10;
		if(jsonData.total%parseInt(showNum,10)!=0){
			length=(jsonData.total/parseInt(showNum,10))+1;
		}else{
			length=jsonData.total/parseInt(showNum,10);
		}
		
		var pageSpan=$("<span></span>");
		var nowPageValue=parseInt(nowPage.val(),10);

		//计算页码显示
		paginate.append(pageSpan);

		if(length>30){
			var sel=$("<select class='ui-state-default' style='width:60px;height:26px;position:relative;top:4px;'></select>");
			for(var i=1;i<=length;i++){
				var option=$("<option value='"+i+"'>"+i+"</option>");
				if(nowPage.val()==i+''){
					option.attr("selected",true);
				}
				sel.append(option);
			}
			sel.on("change",function(){
				var abc_=this.value;
				nowPage.val(abc_);
				pageFuntion(parseInt(abc_,10));
			});
			pageSpan.append(sel);
		}else{
			for(var i=1;i<=length;i++){
				var a=$("<a tabindex='0' class='fg-button ui-button ui-state-default'>"+i+"</a>");
				if(nowPage.val()==i+''){
					a.addClass("ui-state-disabled");
				}else{
					a.on("click",function(){
						var abc_=$(this).html();
						nowPage.val(abc_);
						pageFuntion(parseInt(abc_,10));
					});
				}
				pageSpan.append(a);
			}
		}

		var next=$("<a tabindex='0' class='next fg-button ui-button ui-state-default' id='"+div.attr("id")+"_next'>下一页</a>");
		var last=$("<a tabindex='0' class='last ui-corner-tr ui-corner-br fg-button ui-button ui-state-default' id='"+div.attr("id")+"_last'>最后一页</a>");
		if(nowPage.val()==parseInt(length,10)+''||length==0){
			next.addClass("ui-state-disabled");
			last.addClass("ui-state-disabled");
		}
		paginate.append(next);
		paginate.append(last);

		first.on("click",function(){
			$("#"+json.formid).find("input[name='page']").val(1);
			pageFuntion(1);
		});	
		previous.on("click",function(){
			var input=$("#"+json.formid).find("input[name='page']");
			var page=input.val();
			var inte=parseInt(page,10);
				if(page>1){
					input.val(inte-1);
					pageFuntion(inte-1);
				}else{
					input.val(1);
					pageFuntion(1);
				}
			});
		next.on("click",function(){
			var input=$("#"+json.formid).find("input[name='page']");
			var page=input.val();
			var inte=parseInt(page,10);
				if(inte<parseInt(length,10)){
					input.val(inte+1);
					pageFuntion(inte+1);
				}else{
					input.val(parseInt(length,10));
					pageFuntion(parseInt(length,10));
				}
			});
		last.on("click",function(){
			$("#"+json.formid).find("input[name='page']").val(parseInt(length,10));
			pageFuntion(length);
		});
		$("#select_num").change(function(){
			$("#num").val($("#select_num").val());
			pageFuntion(1);
		});	
		
		if(json.loadAfter){
			json.loadAfter();
		}
	}
	//获得请求路径
	var url=$("#"+json.formid).attr("action");
	
	function pageFuntion(val){
		 $("#"+json.formid+"[name='page']").val(val);
		$.ajax({type:'POST',url:url,dataType:'json',data:$("#"+json.formid).serialize(),success:successFunction});
	}
	pageFuntion(1);
}

