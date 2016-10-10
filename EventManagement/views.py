#-*- coding:utf-8 -*-
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from django.shortcuts import HttpResponse,render_to_response,HttpResponseRedirect,render
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from dtop import settings
import os,statvfs
import models
import json
import time,datetime
import HTMLParser
from Log import logHandle

# Create your views here.

apps = settings.apps
# vfs=os.statvfs('/')
# Size=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)
# Avail=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)
# Used=Size-Avail
# Percent=int(round(round(float(Used)/Size*100,2)))

@login_required
def index(request):
	true_name = request.user.first_name
	return render(request,'em/overview.html',{'apps':apps,'true_name':true_name,'Used':settings.Used,'Size':settings.Size,'Percent':settings.Percent,})

@login_required
def detail(request,detail_id):
	detail_obj = models.Items.objects.get(id=detail_id)
	true_name = request.user.first_name
	handle_info = models.HandleDetail.objects.filter(items_id__id=detail_id).order_by('-handle_time')
	return render(request,'em/detail.html',{'detail_obj':detail_obj,'handle_info':handle_info,'apps':apps,'true_name':true_name,'Used':settings.Used,'Size':settings.Size,'Percent':settings.Percent,})

@login_required
def overview(request):
	page = request.POST.get('page')
	keywords = request.POST.get('keywords')

	if User.objects.get(username=request.user.username).is_superuser:

		if keywords =="":
			if page == "":
				page=1
			items_obj = models.Items.objects.values().order_by('-id')
			# items_total = items_obj.count()
			if int(items_obj.count())%10 !=0:
				page_total = int(items_obj.count())/10 + 1
			else:
				page_total = int(items_obj.count())/10

			items_data = items_obj[(int(page)-1)*10:int(page)*10]
			# data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\"}"
			data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\",\"items_total\":\""+str(items_obj.count())+"\"}"

			return HttpResponse(data)
		else:
			items_obj = models.Items.objects.filter(
	                    Q(items_status__contains=str(keywords)) | Q(items_title__contains=str(keywords)) | Q(items_starter__contains=str(keywords)) \
	                    | Q(items_owner__contains=str(keywords))| Q(items_relater__contains=str(keywords)))

			# items_total = items_obj.count()

			if int(items_obj.count())%10 !=0:
				page_total = int(items_obj.count())/10 + 1
			else:
				page_total = int(items_obj.count())/10

			items_data = items_obj.values().order_by('-id')[(int(page)-1)*10:int(page)*10]
			# data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\"}"
			data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\",\"items_total\":\""+str(items_obj.count())+"\"}"
			return HttpResponse(data)
	else:
		# page = request.POST.get('page')
		# keywords = request.POST.get('keywords')
		# return HttpResponse(keywords)
		if keywords =="":
			if page == "":
				page=1
			items_obj = models.Items.objects.filter(items_owner=request.user.first_name).values().order_by('-id')
			# page_total = items_obj.count()
			if int(items_obj.count())%10 !=0:
				page_total = int(items_obj.count())/10 + 1
			else:
				page_total = int(items_obj.count())/10

			items_data = items_obj[(int(page)-1)*10:int(page)*10]
			# data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\"}"
			data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\",\"items_total\":\""+str(items_obj.count())+"\"}"
			return HttpResponse(data)
		else:
			items_obj = models.Items.objects.filter(items_owner=request.user.first_name).filter(
	                    Q(items_status__contains=str(keywords)) | Q(items_title__contains=str(keywords)) | Q(items_starter__contains=str(keywords)) \
	                    | Q(items_owner__contains=str(keywords))| Q(items_relater__contains=str(keywords)))


			if int(items_obj.count())%10 !=0:
				page_total = int(items_obj.count())/10 + 1
			else:
				page_total = int(items_obj.count())/10

			items_data = items_obj.values().order_by('-id')[(int(page)-1)*10:int(page)*10]
			data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\"}"
			return HttpResponse(data)


#展示用户待办事项与已办事项，具备增删改查权限
@login_required
def Item_list(request,itemstype):
	true_name = request.user.first_name
	if itemstype == 'schedule':
		items_title = '待办事项'
	# elif itemstype == 'done':
	# 	items_title = '已办事项'
	else:
		items_title = '已办事项'
	return render(request,'em/items_normal.html',{'items_title':items_title,'itemstype':itemstype,'apps':apps,'true_name':true_name,'Used':settings.Used,'Size':settings.Size,'Percent':settings.Percent,})

@login_required
def Items_handle(request):
	page = request.POST.get('page')
	itemstype = request.POST.get('itemstype')

	if itemstype == 'schedule':

		items_obj = models.Items.objects.filter(items_owner=request.user.first_name).filter(Q(items_status='进行中') | Q(items_status='逾期/进行中'))

	elif itemstype == 'done':
		items_obj = models.Items.objects.filter(items_owner=request.user.first_name).filter(Q(items_status='已结束') | Q(items_status='逾期/已结束'))

	else:
		items_obj = models.Items.objects.filter(items_relater__contains=request.user.first_name)

	if int(items_obj.count())%10 !=0:
		page_total = int(items_obj.count())/10 + 1
	else:
		page_total = int(items_obj.count())/10

	items_data = items_obj.values().order_by('-id')[(int(page)-1)*10:int(page)*10]
	data = "{\"rows\":"+json.dumps(list(items_data))+",\"page_total\":\""+str(page_total)+"\",\"items_total\":\""+str(items_obj.count())+"\"}"

	return HttpResponse(data)

#展示用户知会事项，只具备查看权限
@login_required
def Items_notice(request):
	true_name = request.user.first_name
	return render(request,'em/notice_overview.html',{'apps':apps,'true_name':true_name,'Used':settings.Used,'Size':settings.Size,'Percent':settings.Percent,})

@login_required
def Notice_detail(request,id):

	detail_obj = models.Items.objects.get(id=id)
	true_name = request.user.first_name
	handle_info = models.HandleDetail.objects.filter(items_id__id=id).order_by('-handle_time')
	return render(request,'em/notice_detail.html',{'detail_obj':detail_obj,'handle_info':handle_info,'apps':apps,'true_name':true_name,'Used':settings.Used,'Size':settings.Size,'Percent':settings.Percent,})



#新建事项
@login_required
def AddItems(request):
	# curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
    # curr_date = datetime.datetime.strptime(curr_date_str,'%Y-%m-%d %H:%M:%S')#将当前时间转换成可加减的日期格式
	
	items_data = request.POST.get("data")
	items_status = items_data.split("&")[0]
	items_title = items_data.split("&")[1]
	items_owner = items_data.split("&")[2]
	start_time = items_data.split("&")[3]
	end_time = items_data.split("&")[4]
	items_relater = items_data.split("&")[5]
	items_content = items_data.split("&")[6]
	items_starter = request.user.first_name
	items_rate = 0
	create_time = time.strftime('%Y-%m-%d %H:%M:%S')

	models.Items.objects.create(items_status=items_status,
		items_title=items_title,
		items_content=items_content,
		items_starter=request.user.first_name,
		items_owner=items_owner,
		items_relater=items_relater,
		create_time=time.strftime('%Y-%m-%d %H:%M:%S'),
		start_time=start_time,
		end_time=end_time,
		items_rate=0
		)

	logHandle.ActionRecord(user_name=request.user.first_name,act_type='新建事项',act_module='事项管理',act_detail='事项标题:'+items_title+';'+ \
		'事项ID:'+str(int(models.Items.objects.get(items_title=items_title).id))+';'+ \
		'事项说明:'+items_content+';'+ \
		'发起人:'+items_starter+';'+ \
		'主办人:'+items_owner+';'+ \
		'知会人:'+items_relater+';'+ \
		'计划开始时间:'+start_time+';'+ \
		'计划结束时间:'+end_time+';' \
		)
	return HttpResponse('1')

#处理事项
@login_required
def TakeItems(request):
	items_data = request.POST.get("data")
	items_id_id= items_data.split("&")[0]
	items_status = items_data.split("&")[1]
	handle_time = items_data.split("&")[2]
	handle_info = items_data.split("&")[3]
	

	#取出时间换成百分百
	Items_obj = models.Items.objects.get(id=items_id_id)
	# for i in Items_obj:
	s_time = datetime.datetime.strptime(str(Items_obj.start_time.encode()),'%Y-%m-%d %H:%M:%S')
	e_time = datetime.datetime.strptime(str(Items_obj.end_time.encode()),'%Y-%m-%d %H:%M:%S')
	h_time = datetime.datetime.strptime(str(handle_time),'%Y-%m-%d %H:%M:%S')

	if h_time < s_time:
		return HttpResponse('0')
	t_time = e_time - s_time
	t_hours = t_time.total_seconds()/3600
	c_time = h_time - s_time
	c_hours = c_time.total_seconds()/3600

	c_rate = (c_time.total_seconds()/3600)/(t_time.total_seconds()/3600)*100



	if c_rate>100:
		# models.Items.objects.filter(id=items_id_id).update(items_status='已逾期',items_rate=-1)
		if items_status =='进行中':
			models.Items.objects.filter(id=items_id_id).update(items_status='逾期/进行中',items_rate=-1)
			models.HandleDetail.objects.create(items_id_id=items_id_id,handle_user=request.user.first_name,handle_time=handle_time,handle_info=handle_info)
		else:
			models.Items.objects.filter(id=items_id_id).update(items_status='逾期/已结束',items_rate=-1)
			models.Items.objects.filter(id=items_id_id).update(finish_time=handle_time,finish_info=handle_info)
	else:
		# models.HandleDetail.objects.create(items_id_id=items_id_id,handle_user=request.user.first_name,handle_time=handle_time,handle_info=handle_info)
		if items_status =='进行中':
			models.Items.objects.filter(id=items_id_id).update(items_status=items_status,items_rate=str(int(c_rate)))
			models.HandleDetail.objects.create(items_id_id=items_id_id,handle_user=request.user.first_name,handle_time=handle_time,handle_info=handle_info)
		else:
			models.Items.objects.filter(id=items_id_id).update(items_status=items_status,finish_time=handle_time,finish_info=handle_info,items_rate=100)
	
	logHandle.ActionRecord(user_name=request.user.first_name,act_type='处理事项',act_module='事项管理',act_detail='事项ID:'+items_id_id+';'+ \
		'处理状态:'+items_status+';'+ \
		'事项状态:'+models.Items.objects.get(id=items_id_id).items_status+';'+ \
		'事项处理时间:'+handle_time+';'+ \
		'事项处理意见:'+handle_info+';'\
		)

	'''
	if items_status =='进行中':
		models.HandleDetail.objects.create(items_id_id=items_id_id,handle_user=request.user.first_name,handle_time=handle_time,handle_info=handle_info)
		if c_rate <100:
			models.Items.objects.filter(id=items_id_id).update(items_rate=str(c_rate))
		else:
			models.Items.objects.filter(id=items_id_id).update(items_status='逾期',items_rate=100)
	else:
		models.Items.objects.filter(id=items_id_id).update(items_status=items_status,finish_time=handle_time,finish_info=handle_info,items_rate=100)
	'''
	return HttpResponse('1')


#数据预处理，返回用户列表供创建新事项选择
@login_required
def Item_init(request):
	user_select =[]
	# user_obj = User.objects.all()
	for items in User.objects.all():
		user_select.append(items.first_name)
	# data = "{\"rows\":"+json.dumps(user_select)+"}"
	data = "{\"rows\":"+json.dumps(user_select)+",\"user\":\""+str(request.user.first_name)+"\"}"
	# data="{\"rows\":"+json.dumps(list(rearch_data.values()))+",\"total\":\""+str(total)+"\",\"record_line\":"+json.dumps(list(record_line))+"}"

	return HttpResponse(data)


#删除数据
@login_required
def DelItems(request):
	del_id = request.POST.get('del_id')
	try:
		models.Items.objects.get(id=del_id)
	except Exception, e:
		return HttpResponse(0)
	else:
		models.Items.objects.filter(id=del_id).delete()
		models.HandleDetail.objects.filter(items_id_id=del_id).delete()
		logHandle.ActionRecord(user_name=request.user.first_name,act_type='删除事项',act_module='事项管理',act_detail='事项ID:'+del_id+';')
		return HttpResponse(1)
	# finally:
	# 	pass
	# if models.Items.objects.get(id=del_id):

	# 	models.Items.objects.filter(id=del_id).delete()
	# 	models.HandleDetail.objects.filter(items_id_id=del_id).delete()
	# 	return HttpResponse(1)
	# else:
	# 	return HttpResponse(0)