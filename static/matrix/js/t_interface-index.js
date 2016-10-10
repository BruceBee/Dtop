var oTable;
$(document).ready(function () {
initModal();
oTable = initTable();
$("#btnEdit").hide();
$("#btnSave").click(_addFun);
$("#btnEdit").click(_editFunAjax);
$("#deleteFun").click(_deleteFun);
//checkboxȫѡ
$("#checkAll").live("click", function () {
    if ($(this).attr("checked") === "checked") {
        $("input[name='checkList']").attr("checked", $(this).attr("checked"));
    } else {
        $("input[name='checkList']").attr("checked", false);
    }
});
});
/**
* ����ʼ��
* @returns {*|jQuery}
*/
function initTable() {
var table = $("#t_interface").dataTable({
	"sAjaxSource": "t_interface-dataList",
	"bPaginate": true,	
	"bLengthChange": true,
	"iDisplayLength": 10,
	"bDestory": true,
	"bRetrieve": true,
	"bFilter": true,
	"bSort": true,
	"Processing": true,
	"aoColumns": [
        {
            "mDataProp": "id",bSortable: false,
            "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                $(nTd).html("<input type='checkbox' name='checkList' value='" + sData + "'>");

            }
		},
        {"mDataProp": "partner_id"},
        {"mDataProp": "partner_name"},
        {"mDataProp": "Sys_id"},
        {"mDataProp": "EntryLog"},
        {"mDataProp": "AppUrl"},
        {"mDataProp": "Configurl"},
        {"mDataProp": "refund_name"}
    ],
    "sDom": "<'row-fluid'<'span6 myBtnBox'><'span6'f>r>t<'row-fluid'<'span6'i><'span6 'p>>",
    "sPaginationType": "bootstrap",
    "oLanguage": {
            "sProcessing": "����������...",
            "sLengthMenu": "��ʾ _MENU_ ����",
            "sZeroRecords": "û��ƥ����",
            "sInfo": "��ʾ�� _START_ �� _END_ �������� _TOTAL_ ��",
            "sInfoEmpty": "��ʾ�� 0 �� 0 �������� 0 ��",
            "sInfoFiltered": "(�� _MAX_ ��������)",
            "sInfoPostFix": "",
            "sSearch": "����:",
            "oPaginate": {
                "sFirst":    "��ҳ",
                "sPrevious": "ǰһҳ",
                "sNext":     "��һҳ",
                "sLast":     "ĩҳ"
            }
    },
    
"fnCreatedRow": function (nRow, aData, iDataIndex) {
        //add selected class
        $(nRow).click(function () {
            if ($(this).hasClass('row_selected')) {
                $(this).removeClass('row_selected');
            } else {
                oTable.$('tr.row_selected').removeClass('row_selected');
                $(this).addClass('row_selected');
            }
        });
    },
    "fnInitComplete": function (oSettings, json) {
        $("#editFun").click(_value);
        $("#addFun").click(_init);
    }

});
return table;
}
 
/**
* ɾ��
* @param id
* @private
**/
function _deleteFun(id) {
var str = '';
var id = '';
$("input[name='checkList']:checked").each(function (i, o) {
    str += $(this).val();
    str += ",";
});
if (str.length > 0) {
    var id = str.substr(0, str.length - 1);
    alert("��Ҫɾ�������ݼ�idΪ" + id);
} else {
    alert("����ѡ��һ����¼����");
}

$.ajax({
    url: "t_interface-deleteFun",
    data: {"id": id},
    type: "post",
    success: function (backdata) {
        if (backdata) {
            oTable.fnReloadAjax(oTable.fnSettings());
        } else {
            alert("ɾ��ʧ��");
        }
    }, error: function (error) {
        console.log(error);
    }
});
}
 
/**
* ��ֵ
* @private
*/
function _value() {
if (oTable.$('tr.row_selected').get(0)) {
    $("#btnEdit").show();
    var selected = oTable.fnGetData(oTable.$('tr.row_selected').get(0));
    $("#column_2").val(selected.partner_id);
    $("#column_3").val(selected.partner_name);
    $("#column_4").val(selected.Sys_id);
    $("#column_5").val(selected.EntryLog);
    $("#column_6").val(selected.AppUrl);
    $("#column_7").val(selected.Configurl);
    $("#column_8").val(selected.refund_name);
    $("#objectId").val(selected.id);
 
    $("#myModal").modal("show");
    $("#btnSave").hide();
} else {
    alert('����ѡ��һ����¼�������');
}
}
 
/**
* �༭���ݴ���ֵ
* @param partner_id, partner_name, Sys_id, EntryLog, AppUrl, Configurl
* @private
*/
function _editFun(partner_id, partner_name, Sys_id, EntryLog, AppUrl, Configurl, refund_name) {
$("#column_2").val(partner_id);
$("#column_3").val(partner_name);
$("#column_4").val(Sys_id);
$("#column_5").val(EntryLog);
$("#column_6").val(AppUrl);
$("#column_7").val(Configurl);
$("#column_8").val(refund_name);
$("#objectId").val(id);
$("#myModal").modal("show");
$("#btnSave").hide();
$("#btnEdit").show();
}
 
/**
* ��ʼ��
* @private
*/
function _init() {
resetFrom();
$("#btnEdit").hide();
$("#btnSave").show();
}
 
/**
* �������
* @private
*/
function _addFun() {
var jsonData = {
    'partner_id': $("#column_2").val(),
    'partner_name': $("#column_3").val(),
    'Sys_id': $("#column_4").val(),
    'EntryLog': $("#column_5").val(),
    'AppUrl': $("#column_6").val(),
    'Configurl': $("#column_7").val(),
    'refund_name': $("#column_8").val()
};
$.ajax({
    url: "t_interface-insertFun",
    data: jsonData,
    type: "post",
    success: function (backdata) {
        if (backdata == 1) {
            $("#myModal").modal("hide");
            resetFrom();
            oTable.fnReloadAjax(oTable.fnSettings());
        } else if (backdata == 0) {
            alert("����ʧ��");
        } else {
            alert("δ֪����");
        }
    }, error: function (error) {
        console.log(error);
    }
});
}
 
 
/*
add this plug in
// you can call the below function to reload the table with current state
Datatablesˢ�·���
oTable.fnReloadAjax(oTable.fnSettings());
*/
$.fn.dataTableExt.oApi.fnReloadAjax = function (oSettings) {
//oSettings.sAjaxSource = sNewSource;
this.fnClearTable(this);
this.oApi._fnProcessingDisplay(oSettings, true);
var that = this;
 
$.getJSON(oSettings.sAjaxSource, null, function (json) {
    /* Got the data - add it to the table */
    for (var i = 0; i < json.aaData.length; i++) {
        that.oApi._fnAddData(oSettings, json.aaData[i]);
    }
    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    that.fnDraw(that);
    that.oApi._fnProcessingDisplay(oSettings, false);
});
}
 
 
/**
* �༭����
* @private
*/
function _editFunAjax() {
var id = $("#objectId").val();
var partner_id = $("#column_2").val();
var partner_name = $("#column_3").val();
var Sys_id = $("#column_4").val();
var EntryLog = $("#column_5").val();
var AppUrl = $("#column_6").val();
var Configurl = $("#column_7").val();
var refund_name = $("#column_8").val();
var jsonData = {
    "id": id,
    "partner_id": partner_id,
    "partner_name": partner_name,
    "Sys_id": Sys_id,
    "EntryLog": EntryLog,
    "AppUrl": AppUrl,
    "Configurl": Configurl,
    "refund_name": refund_name
};

$.ajax({
    type: 'POST',
    url: 't_interface-editFun',
    data: jsonData,
    success: function (json) {
        if (json) {
            $("#myModal").modal("hide");
            resetFrom();
            oTable.fnReloadAjax(oTable.fnSettings());
        } else {
            alert("����ʧ��");
        }
    }
});
}
/**
* ��ʼ��������
*/
function initModal() {
$('#myModal').on('show', function () {
    $('body', document).addClass('modal-open');
    $('<div class="modal-backdrop fade in"></div>').appendTo($('body', document));
});
$('#myModal').on('hide', function () {
    $('body', document).removeClass('modal-open');
    $('div.modal-backdrop').remove();
});
}
 
/**
* ���ñ�
*/
function resetFrom() {
$('form').each(function (index) {
    $('form')[index].reset();
});
}
 
 
/**
* ����ɾ��
* δ��
* @private


function _deleteList() {
var str = '';
$("input[name='checkList']:checked").each(function (i, o) {
    str += $(this).val();
    str += ",";
});
if (str.length > 0) {
    var IDS = str.substr(0, str.length - 1);
    alert("��Ҫɾ�������ݼ�idΪ" + IDS);
} else {
    alert("����ѡ��һ����¼����");
}
}
*/
