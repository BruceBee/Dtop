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
var table = $("#ifappname").dataTable({
	"sAjaxSource": "ifappname-dataList",
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
            "mDataProp": "id", bSortable: false,
            "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                $(nTd).html("<input type='checkbox' name='checkList' value='" + sData + "'>");

            }
		},
        {"mDataProp": "merid"},
        {"mDataProp": "name"},
        {"mDataProp": "ifappname"},
        {"mDataProp": "info"},
        {"mDataProp": "remarks"}
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
                "sPrevious": "��ҳ",
                "sNext":     "��ҳ",
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
    url: "ifappname-deleteFun",
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
    $("#column_2").val(selected.merid);
    $("#column_3").val(selected.name);
    $("#column_4").val(selected.ifappname);
    $("#column_5").val(selected.info);
    $("#column_6").val(selected.remarks);
    $("#objectId").val(selected.id);
 
    $("#myModal").modal("show");
    $("#btnSave").hide();
} else {
    alert('����ѡ��һ����¼�������');
}
}
 
/**
* �༭���ݴ���ֵ
* @param id
* @param name
* @param job
* @param note
* @private
*/
function _editFun(merid, name, ifappname, info, remarks) {
$("#column_2").val(merid);
$("#column_3").val(name);
$("#column_4").val(ifappname);
$("#column_5").val(info);
$("#column_6").val(remarks);
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
    'merid': $("#column_2").val(),
    'name': $("#column_3").val(),
    'ifappname': $("#column_4").val(),
    'info': $("#column_5").val(),
    'remarks': $("#column_6").val()
};
$.ajax({
    url: "ifappname-insertFun",
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
            alert("��ֹ���ݲ�����������Ӱ���ٶȣ�����ɾ��һЩ������������");
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
var merid = $("#column_2").val();
var name = $("#column_3").val();
var ifappname = $("#column_4").val();
var info = $("#column_5").val();
var remarks = $("#column_6").val();
var jsonData = {
    "id": id,
    "merid": merid,
    "name": name,
    "ifappname": ifappname,
    "info": info,
    "remarks": remarks
};
$.ajax({
    type: 'POST',
    url: 'ifappname-editFun',
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
