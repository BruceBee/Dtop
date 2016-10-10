#-*- coding:utf-8 -*-
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtop.settings")# project_name 项目名称
django.setup()
import xlwt
import datetime
import time
from Log import models



def BulidNewExcel():
	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
	    num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	# wb = xlwt.Workbook()
	# ws = wb.add_sheet('Sheet')

	# ws.write(0, 0, 1234.56, style0)
	# ws.write(1, 0, datetime.datetime.now(), style1)
	# ws.write(2, 0, 1)
	# ws.write(2, 1, 1)
	# ws.write(2, 2, xlwt.Formula("A3+B3"))
	# timestr=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	# wb.save('New-'+timestr+'.xls')

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
	wb.save('New-'+timestr+'.xls')
	return timestr

# if __name__ == '__main__':
# 	BulidNewExcel()
