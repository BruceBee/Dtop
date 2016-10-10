// editor:bruce
// time:2016-9-6
//此js基于jquery


function ServerSync(){
    $.ajax({
      type:'POST',
      url:'/OM/ServerSync/',
      data:{'test':'test'},
      dataType:'json',
      success:function(ret){
        // console.log(ret);
        // var serInfo= ret.SerInfo
        // console.log(typeof serInfo)
        // console.log(typeof serInfo.iPhone7)
        for(var p in ret.SerInfo){
          // console.log(p)
          console.log(ret.SerInfo[p].host)
          console.log(ret.SerInfo[p].ipv4)
        }
      },error:function(){
        layer.alert('异常')
      }
    })

  };

//展示服务器组选择
function showGroupSelect(){
    var items = ""
    $("#servergroup option:selected").each(function(){
      items +=$(this).text()+';';
    });
    if(items==""){
    	alert("未选择服务器组")
    }else{
    	$("#group_select_list").html('<hr><input class="btn btn-mini btn-primary pull-right" type="button" value="清除选择" onclick="clearSelect(this);"></input>')
    	$("#group_select_list").append('<span style="color:red">已选服务器组:</span>'+items)    	
    }

  };


//展示服务器选择
function showUserSelect(){
    var items = ""
    $("#serveruser option:selected").each(function(){
      items +=$(this).text()+';';
    });
    $("#user_select_list").html('<hr><input class="btn btn-mini btn-primary pull-right" type="button" value="清除选择" onclick="clearSelect(this);"></input>')
    $("#user_select_list").append('<span style="color:green">已选服务器:</span>'+items)
  };



//查看服务器组详情，修改下属服务器
function showGroupDetail(){
  var count =$("#servergroup option:selected")
  if(count.length == 0){
    layer.alert("请选择对应的服务器组进行查看详情")
  }else if(count.length > 1){
    layer.alert("只能选择一个服务器组进行查看详情")
  }else{
    //获取当前点击的服务器组的id和服务器组名称
    var id = count.val()
    var name = count.text().split("|")[1]
    //第一步，根据id号去后台取出该id号下属的服务器列表，然后展示在可选项的左侧
    //第二步，取出后台所有的可选服务器列表，与第一步的服务器对比去重，然后展示在可选项的右侧
    $.ajax({
      type:'POST',
      url:'/OM/get_serverlist_for_select/',
      data:{'group_id':id},
      dataType:'json',
      success:function(ret){
        $("#groupid").val(id)
        $('#groupid').attr("disabled",true);
        $("#groupname").val(name)
        $("#groupname").attr("disabled",true);
        console.log(ret)
        var members = ret.members_obj
        var all_server = ret.all_server_obj
        console.log(members.length)
        $("#members option").remove();
        $("#unselect option").remove();
        if(members.length != 0){
          for(var i=0;i<members.length;i++){
            $("#members").append("<option value='"+members[i].server_id+"'>"+members[i].server_id+"</option>");
          }
        }
        if(all_server.length != 0){
          for(var i=0;i<all_server.length;i++){
            $("#unselect").append("<option value='"+all_server[i].server_id+"'>"+all_server[i].server_id+"</option>");

              for(var j=0;j<members.length;j++){
                if(all_server[i].server_name == members[j].server_name){
                  $("#unselect option:last").remove();
                  console.log(all_server[i].server_name)
                }
              }
          }
        };

        layer.open({
          title: '查看服务器组详情',
          type: 1,
          skin: 'layui-layer-lan', //样式类名
          area: ['680px', '420px'],
          closeBtn: 1, //不显示关闭按钮
          shift: 2,
          shadeClose: false, //开启遮罩关闭
          btn:['提交','取消'],
          content: $('#GroupAddTable'),
          // content: addTableHtml.html(),
          yes:function(index ){
            var group_id = $("#groupid").val()
            var group_name = $("#groupname").val()
            // var members =$("#members").val()

            var members = ""
            $("#members option").each(function(){
              members +=$(this).text()+';';
            });
            // var members ='test group'
            // layer.alert('提交')
            $.ajax({
              type:'POST',
              url:'/OM/group_modify/',
              data:{'group_id':group_id,'group_name':group_name,'members':members},
              dataType:'text',
              success:function(val){
                layer.close(index);
                layer.alert('修改成功');
                // loadOMgroupinfo();
                if(val=='1'){
                  console.log('获取到了返回值')
                }else{
                  layer.alert(val);
                }
              },error:function(){
                layer.close(index);
                layer.alert("修改失败");
              }
            })
          }
        });
      },error:function(){
        layer.alert('异常')
      }
    })
  // $("#groupid").val()
  // $('#groupid').attr("disabled",false);
  // $("#groupname").val()
  // $("#groupname").attr("disabled",false);

  }
}

//查看服务器详情

function showUserDetail(){
  var count =$("#serveruser option:selected")
  if(count.length == 0){
    layer.alert("请选择对应的服务器进行查看详情")
  }else if(count.length > 1){
    layer.alert("只能选择一个服务器进行查看详情")
  }else{
    // layer.alert(count.val())
    // layer.alert(count.text())
    var server_name = count.text().split('|')[0]
    var server_ip = count.text().split('|')[1]
    var server_memo = $("#serveruser option:selected").attr("memo")
    // layer.alert(server_memo)
    $("#server_name").val(server_name)
    $('#server_name').attr("disabled",true);
    $("#server_ip").val(server_ip)
    $("#server_memo").val(server_memo)

    layer.open({
    title: '查看服务器信息',
    type: 1,
    skin: 'layui-layer-lan', //样式类名
    area: ['360px', '260px'],
    closeBtn: 1, //不显示关闭按钮
    shift: 2,
    shadeClose: false, //开启遮罩关闭
    btn:['提交','取消'],
    content: $('#UserAddTable'),
    yes:function(index ){
      var server_name = $("#server_name").val()
      var server_ip = $("#server_ip").val()
      var server_memo = $("#server_memo").val()
      $.ajax({
        type:'POST',
        url:'/OM/server_modify/',
        data:{'server_name':server_name,'server_ip':server_ip,'server_memo':server_memo},
        dataType:'text',
        success:function(val){
          layer.close(index);
          // layer.alert('添加服务器成功');
          // loadOMgroupinfo();
          if(val=='1'){
            layer.alert('修改服务器成功');
            $("#serveruser option").remove();//先清空
            loadOMuserinfo();//再重新加载
            console.log('获取到了返回值');
          }
          // else{
          //   layer.alert('服务器存在,请重新添加');
          // }
        },error:function(){
          layer.close(index);
          // layer.alert("添加服务器失败");
        }
      })
    }
  });
  }



}

//服务器组全选
function GroupSelectselectAll(){
	$("#servergroup option").each(function(){
      this.selected=true;
    });
  showGroupSelect();
};

//服务组全选

function UserSelectselectAll(){
	$("#serveruser option").each(function(){
      this.selected=true;
    });
  showUserSelect();
};

//服务器组反选
function GroupSelectreverse(){
	$("#servergroup option").each(function(){
      if(this.selected==true){
      	this.selected=false
      }else{
      	this.selected=true
      }
    });
  showGroupSelect();
};

//服务器反选
function UserSelectreverse(){
	$("#serveruser option").each(function(){
      if(this.selected==true){
      	this.selected=false
      }else{
      	this.selected=true
      }
    });
  showUserSelect();
};

//清除服务器组选择
function clearGroupSelect(){
  $("#group_select_list").html("")
  // $("#servergroup").removeAttr("option")
  $("#servergroup option").each(function(){
      this.selected=false;
    });
};


//清除服务器选择
function clearUserSelect(){
  $("#user_select_list").html("")
  $("#serveruser option").each(function(){
      this.selected=false;
    });
};


//清屏
function clearScreen(){
	$("#mainbox").html("[Dartou OM]#<br>")
}


//前端点击运行
function workStart(){
	//获取所选服务器组
	var groupselect=""
	$("#servergroup option:selected").each(function(){
		groupselect+=$(this).text()+';';
	})
	// layer.alert(groupselect)
	//获取所选服务器
	var userselect=""
	$("#serveruser option:selected").each(function(){
		userselect+=$(this).text()+';';
	})
	//获取cmdselect
	var cmdselect=$("#cmdselect option:selected").text();

	//获取argselect
	var argselect=$("#argselect option:selected").text();
	
	// alert("请选择对应的服务器组或者服务器")


	if(groupselect=="" && userselect==""){
		// alert("请选择对应的服务器组或者服务器")
		layer.alert('请选择对应的服务器组或者服务器', {icon: 2});
	}else{
    var pars = $("#cmdselect option:selected").val();
    if(pars=='-1'){
      layer.alert('请选择需要执行的命令', {icon: 2});
    }else{
  		$.ajax({
  			type:'POST',
        		url:'/OM/saltHander/',
        		data:{'groupselect':groupselect,'userselect':userselect,'cmd':cmdselect},
        		cache:false,
        		dataType:'json',
        		success:function(ret){
              console.log(ret);
              $("#mainbox").append('<br>[Dartou OM]#'+cmdselect+'&nbsp;'+argselect+'<br>')
        			for(var i in ret){
                $("#mainbox").append('</span style="color:red;">'+i+'</span>'+'<br>----------<br>')
                $("#mainbox").append(ret[i].replace(/\n/g,'<br/>')+'<br>')
              }
        		},error:function(ret){
        			console.log(ret);
        			$("#mainbox").html('返回失败')
        		}
  		})
    }
	};

};

//前端手动输入命令行
function CMDenter(event){

	var keyCode = event.keyCode?event.keyCode:event.which?event.which:event.charCode;
	if (keyCode ==13){
    var args_text = $("#cmdenter").val();
    var groupselect=""
    var userselect=""
    $("#servergroup option:selected").each(function(){
      groupselect+=$(this).text()+';';
    });
    $("#serveruser option:selected").each(function(){
      userselect+=$(this).text()+';';
    });
    if(groupselect=="" && userselect==""){
      layer.alert('请选择对应的服务器组或者服务器', {icon: 2});
      $("#cmdenter").val("");
    }else{
        var div = document.getElementById('mainbox');
        if(args_text==""){
          $("#mainbox").append('<br>[Dartou OM]#'+args_text+'<br>')
          $("#cmdenter").val("");
        }else{
          $("#mainbox").append('<br>[Dartou OM]#'+args_text+'<br>')
          $.ajax({
            type:'POST',
            url:'/OM/saltHander/',
            data:{'groupselect':groupselect,'userselect':userselect,'cmd':args_text},
            cache:false,
            dataType:'json',
            success:function(ret){
              console.log(ret);
              // console.log(ret.length)
              for(var i in ret){
                // var div = document.getElementById('mainbox');
                // div.innerHTML = div.innerHTML +'</span style="color:red;">'+i+'</span>'+'<br>----------<br>';
                // div.innerHTML = div.innerHTML + ret[i].replace(/\n/g,'<br/>')+'<br>';
                // div.innerHTML = div.innerHTML + '[Dartou OM]##';
                // div.innerHTML = div.innerHTML.slice(-5000,-1)
                // div.scrollTop = div.scrollHeight;

                $("#mainbox").append('<br></span style="color:red;">'+i+'</span>'+'<br>----------<br>');
                $("#mainbox").append(ret[i].replace(/\n/g,'<br/>')+'<br>');
                console.log(ret[i].length)
                // var div = document.getElementById('mainbox');
                // div.innerHTML = div.innerHTML.slice(-5000,-1)
                // div.scrollTop = div.scrollHeight;
                // $("#mainbox").html().slice(-100,-1)
                // $("#mainbox").scrollTop = $("#mainbox").scrollHeight;






                // $("#mainbox").append('</span style="color:red;">'+i+'</span>'+'<br>----------<br>')
                // $("#mainbox").append(ret[i].replace(/\n/g,'<br/>')+'<br>')
                $("#cmdenter").val("");
              }
              $("#mainbox").append('<br>[Dartou OM]#')
            },error:function(ret){
              console.log(ret);
              $("#mainbox").append('<br>输入的指令有误<br>[Dartou OM]#<br>')
              $("#cmdenter").val("");
            }
          })
        }
      // var div = document.getElementById('mainbox');
      div.innerHTML = div.innerHTML.slice(-500000,-1)
      div.scrollTop = div.scrollHeight;

      }
    }
  };



//新建、删除服务器组和服务器
function item_action(ths){
  var layer_select = ths.getAttribute('value');
  $("#groupid").val("")
  $('#groupid').attr("disabled",false);
  $("#groupname").val("")
  $("#groupname").attr("disabled",false);
  $("#members option").remove();

  $("#server_name").val("")
  $("#server_name").attr("disabled",false);
  $("#server_ip").val("")
  $("#server_memo").val("")

  // $.ajax({
  //     type:'POST',
  //     url:'/OM/get_serverlist_for_select/',
  //     data:{'group_id':'00001'},
  //     dataType:'json',
  //     success:function(ret){
  //       console.log(ret)
  //       var members = ret.members_obj
  //       var all_server = ret.all_server_obj
  //       console.log(members.length)
  //       // $("#members option").remove();
  //       $("#unselect option").remove();
  //       if(all_server.length != 0){
  //         for(var i=0;i<all_server.length;i++){
  //           $("#unselect").append("<option value='"+all_server[i].server_id+"'>"+all_server[i].server_name+"</option>");
  //         }
  //       };
  //     }
  // });
  // $("#unselect option:last").remove();

  if(layer_select == 'group_add'){
    $.ajax({
        type:'POST',
        url:'/OM/get_serverlist_for_select/',
        data:{'group_id':'00001'},
        dataType:'json',
        success:function(ret){
          console.log(ret)
          var members = ret.members_obj
          var all_server = ret.all_server_obj
          console.log(members.length)
          // $("#members option").remove();
          $("#unselect option").remove();
          if(all_server.length != 0){
            for(var i=0;i<all_server.length;i++){
              $("#unselect").append("<option value='"+all_server[i].server_id+"'>"+all_server[i].server_name+"</option>");
            }
          };
        }
    });

    layer.open({
    title: '新建服务器组',
    type: 1,
    skin: 'layui-layer-lan', //样式类名
    area: ['680px', '420px'],
    closeBtn: 1, //不显示关闭按钮
    shift: 2,
    shadeClose: false, //开启遮罩关闭
    btn:['提交','取消'],
    content: $('#GroupAddTable'),
    yes:function(index ){
      var group_id = $("#groupid").val()
      var group_name = $("#groupname").val()
      // var members =$("#members").val()

      var members = ""
            $("#members option").each(function(){
              members +=$(this).text()+';';
            });
      // if(members==""){
      //   layer.alert("至少选择一台下属服务器");
      // }
      // var members ='test group'
      // layer.alert('提交')
      $.ajax({
        type:'POST',
        url:'/OM/group_add/',
        data:{'group_id':group_id,'group_name':group_name,'members':members},
        dataType:'text',
        success:function(val){
          layer.close(index);
          // loadOMgroupinfo();
          if(val=='1'){
            layer.alert("添加成功");
            $("#servergroup option").remove();//先清空
            loadOMgroupinfo();//再重新加载
          }else{
            layer.alert(val);
          }
        },error:function(){
          layer.close(index);
          layer.alert("添加失败");
        }
      })
    }
  });

  }else if(layer_select == 'group_del'){
    $.ajax({
        type:'POST',
        url:'/OM/get_all_groups_list/',
        data:'null',
        dataType:'json',
        success:function(ret){
          console.log(ret)
          // var members = ret.members_obj
          var servergroup = ret.servergroup_obj
          // console.log(members.length)
          // $("#members option").remove();
          $("#groupdel option").remove();
          if(servergroup.length != 0){
            for(var i=0;i<servergroup.length;i++){
              $("#groupdel").append("<option value='"+servergroup[i].servergroup_id+"'>"+servergroup[i].servergroup_id+'|'+servergroup[i].servergroup_name+"</option>");
            }
          };
        }
    });


    layer.open({
    title: '删除服务器组',
    type: 1,
    skin: 'layui-layer-lan', //样式类名
    area: ['360px', '500px'],
    closeBtn: 1, //不显示关闭按钮
    shift: 2,
    shadeClose: false, //开启遮罩关闭
    btn:['提交','取消'],
    content: $('#GroupDelTable'),
    yes:function(index){
      var groupdel = ""
      $("#groupdel option:selected").each(function(){
      groupdel +=$(this).text()+';';
      });
      $.ajax({
        type:'POST',
        url:'/OM/group_del/',
        data:{'group_del':groupdel},
        dataType:'text',
        success:function(val){
          layer.close(index);
          // loadOMgroupinfo();
          if(val=='1'){
            console.log('获取到了返回值');
            layer.alert('删除成功');
            $("#servergroup option").remove();//先清空
            loadOMgroupinfo();//再重新加载
          }else{
            layer.alert(val);
          }
        },error:function(){
          layer.close(index);
          layer.alert("删除失败");
        }
      })
    }
  });

  }else if(layer_select == 'server_add'){
    layer.open({
    title: '新建服务器',
    type: 1,
    skin: 'layui-layer-lan', //样式类名
    area: ['360px', '260px'],
    closeBtn: 1, //不显示关闭按钮
    shift: 2,
    shadeClose: false, //开启遮罩关闭
    btn:['提交','取消'],
    content: $('#UserAddTable'),
    yes:function(index ){
      var server_name = $("#server_name").val()
      var server_ip = $("#server_ip").val()
      var server_memo = $("#server_memo").val()
      $.ajax({
        type:'POST',
        url:'/OM/server_add/',
        data:{'server_name':server_name,'server_ip':server_ip,'server_memo':server_memo},
        dataType:'text',
        success:function(val){
          layer.close(index);
          // layer.alert('添加服务器成功');
          // loadOMgroupinfo();
          if(val=='1'){
            layer.alert('添加服务器成功');
            $("#serveruser option").remove();//先清空
            loadOMuserinfo();//再重新加载
            console.log('获取到了返回值');
          }else{
            layer.alert('服务器存在,请重新添加');
          }
        },error:function(){
          layer.close(index);
          layer.alert("添加服务器失败");
        }
      })
    }
  });

  }else{
    $.ajax({
        type:'POST',
        url:'/OM/get_all_server_list/',
        data:'null',
        dataType:'json',
        success:function(ret){
          console.log(ret)
          // var members = ret.members_obj
          var serveruser_obj = ret.serveruser_obj
          // console.log(members.length)
          // $("#members option").remove();
          $("#serverdel option").remove();
          if(serveruser_obj.length != 0){
            for(var i=0;i<serveruser_obj.length;i++){
              $("#serverdel").append("<option value='"+serveruser_obj[i].server_id+"'>"+serveruser_obj[i].server_name+'|'+serveruser_obj[i].server_ip+"</option>");
            }
          };
        }
    });

    layer.open({
    title: '删除服务器',
    type: 1,
    skin: 'layui-layer-lan', //样式类名
    area: ['360px', '500px'],
    closeBtn: 1, //不显示关闭按钮
    shift: 2,
    shadeClose: false, //开启遮罩关闭
    btn:['提交','取消'],
    content: $('#UserDelTable'),
    yes:function(index ){
      var serverdel = ""
      $("#serverdel option:selected").each(function(){
        serverdel +=$(this).text()+';';
        });
      $.ajax({
        type:'POST',
        url:'/OM/server_del/',
        data:{'server_del':serverdel},
        dataType:'text',
        success:function(val){
          layer.close(index);
          // layer.alert('删除服务器成功');
          // loadOMgroupinfo();
          if(val=='1'){
            console.log('获取到了返回值');
            layer.alert('删除服务器成功');
            $("#serveruser option").remove();//先清空
            loadOMuserinfo();//再重新加载
            // console.log('获取到了返回值');
          }else{
            layer.alert(val);
          }
        },error:function(){
          layer.close(index);
          layer.alert("删除服务器失败");
        }
      })
    }
  });
  }
};



//加载服务器组信息
function loadOMgroupinfo(){
  // document.getElementById("servergroup").options.length=0;
  var url ='/OM/LoadGroupInfo/';
  var myAjax = new Ajax.Request(
    url,
    {
      method:'get',
      onComplete:showResponse
    });
  function showResponse(originalRequest){
    var html = originalRequest.responseText;
    var objarray = html.split(";");
    for ( var i=0;i<html.split(";").length-1;i++){
      var oOption = document.createElement('OPTION');
      oOption.value = objarray[i].split(',')[0];//id
      oOption.text = oOption.value+'|'+objarray[i].split(',')[1];//内容,实际显示部分
      document.servergroupForm.servergroup.options.add(oOption);
    }
  }
};



//加载服务器列表信息
function loadOMuserinfo(){
  var url ='/OM/LoadOMUserInfo/';
  var myAjax = new Ajax.Request(
    url,
    {
      method:'get',
      onComplete:showResponse
    });
  function showResponse(originalRequest){
    // alert('1')
    // alert(originalRequest.responseText);
    // console.log(originalRequest.responseText)
    var html = originalRequest.responseText;
    var objarray = html.split(";");
    // alert('2')
    // var options_value = objarray.split(',')[0];
    // var options_text = objarray.split(',')[1];
    // alert('3')
    for ( var i=0;i<html.split(";").length-1;i++){
      var oOption = document.createElement('OPTION');
      oOption.value = objarray[i].split(',')[0];//name
      // oOption.memo = objarray[i].split(',')[2];//name
      oOption.setAttribute("memo",objarray[i].split(',')[2])//添加memo自定义属性
      oOption.text = oOption.value+'|'+objarray[i].split(',')[1];//ip,实际显示部分
      document.serveruserForm.serveruser.options.add(oOption);
    }
  }

};


