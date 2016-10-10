#-*- coding:utf-8 -*-
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# from DataDownload import BulidExcel
# from django.db.models import get_model
from Log import models
import datetime
import xlwt


# def build_om_excel():

# 	ret = BulidExcel.BulidNewExcel()
# 	return ret

def BulidNewExcel(download_url):
	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
	    num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
	#获取字段名(列表)
	field_name_list = []
	for i in models.SSHLog._meta.get_fields():
		field_name_list.append(i._verbose_name)
	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	wb = xlwt.Workbook()
	ws = wb.add_sheet('Sheet',cell_overwrite_ok=True)
	for i in range(len(field_name_list)):
		ws.write(0,i,field_name_list[i],style0)

	mylist=[]

	log_obj = models.SSHLog.objects.all()

	for i in log_obj.values():
		mylist.append([i['id'],i['client_ip'],i['cmd_server_group_id'],i['cmd_server_server_id'],i['cmd_time'],i['cmd_user'],i['cmd_command']])

	for i in range(0,log_obj.count()):
		for j in range(len(field_name_list)):
			ws.write(i+1,j,mylist[i][j])
	timestr=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	# return timestr
	wb.save(download_url+'New-'+timestr+'.xls')
	return timestr