# -*- coding: utf-8 -*-

import xlrd,xlwt

def set_style(name,hight,bold=False):
	style = xlwt.XFStyle()

	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.hight = hight


	style.font = font

	return style


def write_excel():
	f = xlwt.Workbook(encoding='utf-8')

	sheet1 = f.add_sheet(u'sheet1')
	row0 = [u'业务',u'状态',u'北京',u'上海',u'广州',u'深圳',u'状态小计',u'合计']
	column0 = [u'机票',u'船票',u'火车票',u'汽车票',u'其它']
	status = status = [u'预订',u'出票',u'退票',u'业务小计']


	for i in range(0,len(row0)):
		sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))

	i, j = 1, 0
  	while i < 4*len(column0) and j < len(column0):

	    sheet1.write_merge(i,i+3,0,0,column0[j],set_style('Arial',220,True)) #第一列
	    sheet1.write_merge(i,i+3,7,7) #最后一列"合计"
	    i += 4
	    j += 1
 
  	sheet1.write_merge(21,21,0,1,u'合计',set_style('Times New Roman',220,True))
 
  #生成第二列
  	i = 0
	while i < 4*len(column0):
	  for j in range(0,len(status)):
	    sheet1.write(j+i+1,1,status[j])
	  i += 4
	 
	f.save('demo2.xls') #保存文件

if __name__ == '__main__':
  #generate_workbook()
  #read_excel()
  write_excel()