# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse,render_to_response,HttpResponseRedirect,render
from django.template import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,Group,Permission
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods,require_POST,require_GET
import os,sys,commands,subprocess,re,zipfile,shutil,statvfs,MySQLdb as mdb,json,chardet
import difflib,datetime,time,threading,urllib2,json,string
from datetime import date
from django.views.generic import TemplateView
from django import forms
from forms import DnsForm
from qiniu import Auth, put_data, put_file
from django.http import StreamingHttpResponse
from random import *
from Matrix import models
from django.core import serializers
from check_permission import check_permission
from permissionchecklist import settings
from Log import logHandle
from download.core import FileHandle
from EventManagement.models import Items
##################################################################################

reload(sys)
sys.setdefaultencoding('utf-8')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=1000000)
    file = forms.FileField()

def favicon(request):
    return HttpResponseRedirect('/images/favicon.ico')

def login(request):
    if not request.user.is_authenticated():
        return render_to_response('auth.html',context_instance=RequestContext(request))
    else:
        # logHandle.ActionRecord(user_name=request.user.first_name,act_detail='login')
        return HttpResponseRedirect('home/dashboard.html')
        # return HttpResponse('yes')

def Vre(string):
    return str(string).strip().replace('&','&amp;').replace('>','&gt;').replace('<','&lt;').replace('"','&quot;').replace('\n','\r\n')

def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)



def UTC_to_Local(uct_time):
    time_offset=datetime.timedelta(hours=8)
    local_time = uct_time + time_offset
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

LOGIN_TOKEN='16080,94a8f63fc836d76ceb76ab4cdb36ee78'

@never_cache
@require_POST
def auth(request):
    print get_client_ip(request)
    x_message="您的请求已被拦截01！"
    request.session['x_message']=x_message
    if request.method == 'POST':
        username = Vre(request.POST.get('username', ''))
        password = Vre(request.POST.get('password', ''))
        uname = Vre(request.POST.get('uname', ''))
        tname = Vre(request.POST.get('tname', ''))
        if (not username or not password) and (not uname or not tname):
            return HttpResponse(x_message)
        else:
            try:#本地库验证
                if username and password:
                    u=User.objects.get(username__exact=username)
                elif uname and tname:#重置密码
                    try:
                        u=User.objects.get(Q(username__exact=uname),Q(first_name__exact=tname))
                        try:
                            characters=string.ascii_letters + string.digits
                            password="".join(choice(characters) for x in range(randint(6, 6)))
                            u.set_password(password)
                            u.save()
                            return HttpResponseRedirect('auth.html?error=N')
                        except:
                            return HttpResponseRedirect('auth.html?error=v')
                    except:
                        return HttpResponseRedirect('auth.html?error=v')

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        request.session.set_expiry(28800)
                    else:
                        return HttpResponseRedirect('auth.html?error=Y')
                else:
                    return HttpResponseRedirect('auth.html?error=V')
            except:
                return HttpResponseRedirect('auth.html?error=V')

            if request.user.is_authenticated():
                logHandle.ActionRecord(user_name=request.user.first_name,act_type='login',act_detail='登录')
                try:
                    if password.isdigit() and len(password) <= 6:
                        redirect_to='V/password_change/'
                    else:
                        redirect_to=request.META.get('HTTP_REFERER', False).lstrip('/').strip().split('next')[1].split('=')[1]
                except:
                    redirect_to='home/dashboard.html'
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponse(x_message)
# @check_permission
@login_required
@require_GET
def index(request):
    #权限管理入口
    # return HttpResponse(request.get_full_path())
    print get_client_ip(request)
    global Size,Used,Percent,apps,appname,appgroup,true_name,last_login,base_id
    x_message=request.session.get('x_message',"您的请求已被拦截02！")
    V=request.get_full_path().lstrip('/').strip()
    try:
        if len(V.split('.')) != 2 or V.split('.')[1].split('?')[0] != 'html':return HttpResponse(x_message)
        try:
            base_id=V.split('.')[1].split('?')[1].split('&&')[0].split('=')[1]
        except:
            base_id=''
    except:
        return HttpResponse(x_message)
    vfs=os.statvfs('/')
    Size=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)
    Avail=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)
    Used=Size-Avail
    Percent=int(round(round(float(Used)/Size*100,2)))
    appname=V.split('/')[1].split('.')[0]
    appgroup=V.split('/')[0]
    apps={'dashboard':{'url':'/home/dashboard.html','name':'开始'},
        'baseinfo':{'url':'/info/baseinfo.html','name':'云资源信息'},
        'hostconfig':{'url':'/info/hostconfig.html','name':'主机配置信息'},
        'businessinfo':{'url':'/info/businessinfo.html','name':'业务线配置信息'},
        'platforminfo':{'url':'/info/platforminfo.html','name':'云平台配置信息'},
        'assetinfo':{'url':'/asset/assetinfo.html','name':'硬件资产信息'},
        'autorelease':{'url':'/auto/autorelease.html','name':'项目发布回滚'},
        'domaininfo':{'url':'/dns/domaininfo.html','name':'域名信息'},
        'dnsinfo':{'url':'/dns/dnsinfo.html','name':'DNS信息'},
        'autodnspod':{'url':'/auto/autodnspod.html','name':'DNS数据同步'},
        'alarminfo':{'url':'/alarm/alarminfo.html','name':'告警日志'},
        'alarmcharts':{'url':'/alarm/alarmcharts.html','name':'告警统计'},
        'usermanagement':{'url':'/auth/usermanagement.html','name':'用户管理'},
        'groupsmanagement':{'url':'/auth/groupsmanagement.html','name':'用户组管理'},
        'wooyunsearch':{'url':'/link/wooyunsearch.html','name':'乌云一下'},
        'om':{'url':'/OM/','name':'运维管理'},
        'em':{'url':'/em/','name':'事项管理'},
        }

    if not apps.has_key(appname):return HttpResponse(x_message)

    if not request.user.is_authenticated():
        return HttpResponseRedirect(LOGIN_URL)
    else:
        true_name=request.user.first_name
        if not true_name:true_name=request.user.username
        return render_to_response(V.split('?')[0],{'true_name':true_name,'Used':Used,'Size':Size,'Percent':Percent,'apps':apps,'appname':appname,'appgroup':appgroup},\
            context_instance=RequestContext(request))




# def om(request):
#     return render_to_response('/om/OMindex.html')
@login_required
def loadDashboard(request):
    if request.method == "POST":
        curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
        curr_date = datetime.datetime.strptime(curr_date_str,'%Y-%m-%d %H:%M:%S')#将当前时间转换成可加减的日期格式
        
        text = request.POST.get('text')

        baseinfo_count = models.BaseInfo.objects.all().count()
        configinfo_count = models.ConfigInfo.objects.all().count()
        businessinfo_count = models.BusinessUnit.objects.all().count()
        platforminfo_count = models.Platform.objects.all().count()

        assetinfo = models.Asset.objects.all()
        assetinfo_count = assetinfo.count()
        assetinfo_type = assetinfo.values('device_type').distinct().count()
        assetinfo_user = assetinfo.values('device_user').distinct().count()
        assetinfo_dept = assetinfo.values('device_dept').distinct().count()


        domaininfo_count = models.DomainInfo.objects.all().count()
        dnsinfo_count = models.DnsInfo.objects.all().count()

        one_hour_ok,one_hour_problem=AlertDataInquery(curr_date,curr_date_str,hours=-1)
        one_day_ok,one_day_problem=AlertDataInquery(curr_date,curr_date_str,hours=-24)

        user_obj = User.objects.all()
        user_count = user_obj.count()
        superuser_count = user_obj.filter(is_superuser=True).count()
        group_count = Group.objects.all().count()


        user_dict ={}
        user_str=''
        # x = User.objects.all().values().order_by('-last_login')
        for i in User.objects.all().order_by('-last_login')[0:5]:
            aa = UTC_to_Local(i.last_login)
            user_dict[i.username] = {}
            user_dict.update({i.username:i.first_name+'+'+str(UTC_to_Local(i.last_login))})
            user_str+=i.username+','+i.first_name+','+str(UTC_to_Local(i.last_login))+'|'
            # x[i]['last_login'] = str(UTC_to_Local(i['last_login']))

        Items.objects.filter(items_status='未开始').filter(start_time__lte=curr_date_str.decode()).update(items_status ='进行中')

        Items.objects.filter(items_status='进行中').filter(end_time__lte=curr_date_str.decode()).update(items_status ='逾期/进行中')
        
        items_schedule_obj = Items.objects.filter(items_owner=request.user.first_name).filter(Q(items_status='进行中') | Q(items_status='逾期/进行中'))
        items_done_obj = Items.objects.filter(items_owner=request.user.first_name).filter(Q(items_status='已结束') | Q(items_status='逾期/已结束'))
        items_notice_obj = Items.objects.filter(items_relater__contains=request.user.first_name)


        items_schedule = items_schedule_obj.count()
        if items_schedule == 0:
            items_schedule_last="当前无待办事项"
            items_schedule_last_id = 0
        else:
            for i in items_schedule_obj.order_by('-id')[0:1]:
                items_schedule_last = i.items_title
                items_schedule_last_id = i.id


        items_done = items_done_obj.count()
        if items_done == 0:
            items_done_last="当前无已办事项"
            items_done_last_id = 0
        else:
            for i in items_done_obj.order_by('-id')[0:1]:
                items_done_last = i.items_title
                items_done_last_id = i.id

        
        items_notice = items_notice_obj.count()
        if items_notice == 0:
            items_notice_last="当前无知会事项"
            items_notice_last_id = 0
        else:
            for i in items_notice_obj.order_by('-id')[0:1]:
                items_notice_last = i.items_title
                items_notice_last_id = i.id   


        domain_dict = {'baseinfo_count':baseinfo_count,
                'configinfo_count':configinfo_count,
                'businessinfo_count':businessinfo_count,
                'platforminfo_count':platforminfo_count,
                'assetinfo_count':assetinfo_count,
                'domaininfo_count':domaininfo_count,
                'dnsinfo_count':dnsinfo_count,
                'assetinfo_type':assetinfo_type,
                'assetinfo_user':assetinfo_user,
                'assetinfo_dept':assetinfo_dept,
                'one_hour_problem':one_hour_problem,
                'one_hour_ok':one_hour_ok,
                'one_day_problem':one_day_problem,
                'one_day_ok':one_day_ok,
                'user_count':user_count,
                'group_count':group_count,
                'superuser_count':superuser_count,
                'last_login':user_str,
                'items_schedule':items_schedule,
                'items_done':items_done,
                'items_notice':items_notice,
                'items_schedule_last':items_schedule_last,
                'items_done_last':items_done_last,
                'items_notice_last':items_notice_last,
                'items_schedule_last_id':items_schedule_last_id,
                'items_done_last_id':items_done_last_id,
                'items_notice_last_id':items_notice_last_id,
                }

        data = "{\"rows\":"+json.dumps(domain_dict)+"}"
        return HttpResponse(data)




# @check_permission
@login_required
@require_POST
# @permission_required('change_contenttype')
def auto_data(request):
    x_message=request.session.get('x_message',"您的请求已被拦截04！")
    if len(request.get_full_path().lstrip('/').strip().split('/')[1].split('_')) < 2:
        return HttpResponse(x_message)
    dbname=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[0]
    action=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[1]

    if action == 'putdata':
        if request.method == 'POST':
            f = request.FILES['schid_file']
            file_name = f.name
            f_path='/tmp/'+file_name
        else:
            return HttpResponse(x_message)
        if file_name:
            if os.path.isfile(f_path):
                #urllib2.urlopen(url)
                #Vlog('"[success] '+time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time()))+' '+get_client_ip(request)+' '+request.user.first_name+' 
                #上传模板已存在（stbname：'+str(f.name)+'）"')
                return HttpResponse("<font color=green>云端已存在此文件，将跳过上传步骤</font>")
            else:
                paths = file_name.split('.')
                if paths[1] == 'zip':
                    if 1:
                        with open(f_path, 'wb+') as info:
                            for chunk in f.chunks():
                                info.write(chunk)

                        ress = '<font color=green>文件 '+file_name+' 已成功上传至云端</font>'
                        #Vlog('"[success] '+time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time()))+' '+get_client_ip(request)+' '+request.user.first_name+' 
                        #上传模板成功（stbname：'+ss+'）"')
                        return HttpResponse(ress)
                    #except:
                    #    res = 0
                        #Vlog('"[error] '+time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time()))+' '+get_client_ip(request)+' '+request.user.first_name+' 
                        #上传模板失败（stbname：'+ss+'）"')
                    #    return HttpResponse(res)
                else:
                    res = 0
                    return HttpResponse(res)
        else:
            return HttpResponse(x_message)

    elif action == 'sync' and request.user.has_perm('delete_contenttype'):
        if dbname == 'domainlist':
            #API获取DNSPod的DomainList,入库
            CMD="curl -sX POST https://dnsapi.cn/Domain.List -d 'login_token="+LOGIN_TOKEN+"&format=json'"
            raw_data=commands.getoutput(CMD)
            req=json.loads(raw_data)
            ret={}

            for i in range(len(req['domains'])):
                DD={'domain_id':req['domains'][i]['id'],'domain_status':req['domains'][i]['status'],'domain_name':req['domains'][i]['name'],\
                'domain_records':req['domains'][i]['records'],'domain_remark':req['domains'][i]['remark'],'domain_grade':req['domains'][i]['grade'],}

                try:
                    objects, created = models.DomainInfo.objects.update_or_create(domain_id=DD['domain_id'],defaults=DD)
                    flag=('created' if created else 'updated')
                except Exception as e:
                    flag=e
                ret[str(DD['domain_id'])]=DD['domain_name'],flag

            delret={}
            for j in models.DomainInfo.objects.all():
                if not ret.has_key(j.domain_id):
                    models.DomainInfo.objects.filter(domain_id=j.domain_id).delete()
                    delret[j.domain_id]=j.domain_name,'deleted'

            result=dict(ret, **delret)
            # return HttpResponse(json.dumps(result))
        
            #API获取dnspod的线路列表和类型列表，入库
            
            domain_obj = models.DomainInfo.objects.all()
            recordslinelist={}
            recordstypelist={}
            for i in domain_obj:
                recordsline_CMD = "curl -sX POST https://dnsapi.cn/Record.Line -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_grade="+i.domain_grade+"&domain_id="+i.domain_id+"'"
                recordstype_CMD = "curl -sX POST https://dnsapi.cn/Record.Type -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_grade="+i.domain_grade+"'"
                
                recordsline_data=commands.getoutput(recordsline_CMD)
                recordstype_data=commands.getoutput(recordstype_CMD)
                
                recordsline_req=json.loads(recordsline_data)
                recordstype_req=json.loads(recordstype_data)

                recordslinelist[str(i)]=recordsline_req
                
                recordstypelist[str(i)]=recordstype_req
                recordstypelist[str(i)]['name']=i.domain_name
                recordstypelist[str(i)]['grade']=i.domain_grade
            #获取domian信息表中domain_id与domian_grade,通过api获取对应的线路列表，写入DomainRecordLine表里
            for line_key in recordslinelist:
                #key = 9个域名
                for line_kk in recordslinelist[line_key]:
                    for line_r in range(len(recordslinelist[line_key]['lines'])):
                        line_ids = recordslinelist[line_key]['lines'][line_r]
                        # line_zone = line_ids
                        line_value= recordslinelist[line_key]['line_ids'][line_ids]
                        line_dict = {'Domain_id':str(line_key),'record_lines_ids':line_ids.encode("utf8"),'record_zone':line_ids.encode("utf8"),'record_line_id':line_value,}
                        models.DomainRecordLine.objects.update_or_create(**line_dict)


                    #recordslinelist[key] =dartou.com
                    #kk = 三种(免费套餐)或者四种(旗舰套餐)
                    if recordslinelist[line_key].has_key('line_groups'):
                        for line_r in range(len(recordslinelist[line_key]['line_groups'])):
                            line_ids = recordslinelist[line_key]['line_groups'][line_r]['name']
                            # bbb = "测试"
                            line_zone = ""
                            for line_m in range(len(recordslinelist[line_key]['line_groups'][line_r]['lines'])):
                                line_zone+=recordslinelist[line_key]['line_groups'][line_r]['lines'][line_m]+','

                            line_value = recordslinelist[line_key]['line_groups'][line_r]['line_id']

                            line_group_dict = {'Domain_id':str(line_key),'record_lines_ids':line_ids.encode("utf8"),'record_zone':line_zone.encode("utf8"),'record_line_id':line_value,}

                            DomainRecordLine_obj = models.DomainRecordLine.objects.filter(Domain_id=line_group_dict['Domain_id'],record_lines_ids=line_group_dict['record_lines_ids'])

                            if DomainRecordLine_obj:DomainRecordLine_obj.update(**line_group_dict)
                            else:models.DomainRecordLine.objects.create(**line_group_dict)
            #获取domian信息表中domain_id对应的domian_grade,通过api获取对应的类型列表，写入DomainRecordType表里
            for type_key in recordstypelist:
                domain_name = recordstypelist[type_key]['name']
                domain_grade = recordstypelist[type_key]['grade']
                for type_kk in recordstypelist[type_key]:
                    for l in range(len(recordstypelist[type_key]['types'])):
                        record_type = recordstypelist[type_key]['types'][l]
                        type_dict = {'domain_name':domain_name.encode("utf8"),'domain_grade':domain_grade.encode("utf8"),'record_type':record_type.encode("utf8")}

                        DomainRecordType_obj = models.DomainRecordType.objects.filter(domain_name=type_dict['domain_name'],domain_grade=type_dict['domain_grade'],record_type=type_dict['record_type'])

                        if DomainRecordType_obj:pass
                        else:models.DomainRecordType.objects.create(**type_dict)

            return HttpResponse(json.dumps(result))
            # return HttpResponse(json.dumps(recordstypelist))

        elif dbname == 'recordlist':
            domain_id=Vre(request.POST.get('domain_id', ''))
            CMD="curl -sX POST https://dnsapi.cn/Record.List -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id="+domain_id+"'"
            raw_data=commands.getoutput(CMD)
            req=json.loads(raw_data)
            ret={}
            Domain_name_id=int(models.DomainInfo.objects.get(domain_id=domain_id).id)
            dnsop=Vre(request.POST.get('dnsop', '无名氏'))
            for i in range(len(req['records'])):
                DD={'dns_id':req['records'][i]['id'],'dns_name':req['records'][i]['name'],'dns_type':req['records'][i]['type'],'dns_line':req['records'][i]['line'],\
                'dns_value':req['records'][i]['value'],'dns_weight':req['records'][i]['weight'],'dns_mx':req['records'][i]['mx'],'dns_ttl':req['records'][i]['ttl'],\
                'dns_enabled':req['records'][i]['enabled'],'dns_remark':req['records'][i]['remark'],'dns_updated_on':req['records'][i]['updated_on'],\
                'dnsop':dnsop,'Domain_name_id':Domain_name_id,}
                try:
                    objects, created = models.DnsInfo.objects.update_or_create(dns_id=DD['dns_id'],defaults=DD)
                    flag=('created' if created else 'updated')
                except Exception as e:
                    flag=e
                ret[str(DD['dns_id'])]=DD['dns_name'],DD['dns_value'],flag

            return HttpResponse(json.dumps(ret))
        else:
            return HttpResponse(x_message)
    else:
        return HttpResponse(x_message)


# @check_permission
@login_required
@require_POST
# @permission_required('add_contenttype')
def dns_data(request):
    x_message=request.session.get('x_message',"您的请求已被拦截05！")
    if len(request.get_full_path().lstrip('/').strip().split('/')[1].split('_')) < 2:
        return HttpResponse(x_message)
    dbname=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[0]
    action=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[1]
    
    V=request.get_full_path().lstrip('/').strip()
    try:
        dns_id=V.split('.')[1].split('?')[1].split('=')[1]
    except:
        dns_id=''

    if dbname == 'domaininfo':
        if action == 'pagedataList':
            tj=Vre(request.POST.get('tj', ''))

            # return HttpResponse(request.get_full_path())
            page=int(request.POST.get('page', '1').encode('latin-1', 'ignore').strip())
            num=int(request.POST.get('num', '10').encode('latin-1', 'ignore').strip())

            domain_data=models.DomainInfo.objects.values()[(page-1)*num:page*num]
            record_line=models.DomainRecordLine.objects.values().all()
            record_type=models.DomainRecordType.objects.values().all()
            #遍历将每个实例的domain_id进行组合url重新赋值，url部分对应dns相关的处理函数
            for item in domain_data:
                item['domain_id'] = '<a href="/dns/dnsinfo.html?dns_id='+str(item['id'])+'">'+item['domain_id']+'</a>'

            #搜索模块

            if tj=="":
                total = models.DomainInfo.objects.count()
                # data="{\"rows\":"+json.dumps(list(domain_data))+",\"total\":\""+str(total)+"\"}"
                data="{\"rows\":"+json.dumps(list(domain_data))+",\"total\":\""+str(total)+"\",\"record_line\":"+json.dumps(list(record_line))+",\"record_type\":"+json.dumps(list(record_type))+"}"
                return HttpResponse(data)
            else:
                rearch_data = models.DomainInfo.objects.filter(
                    Q(domain_id__contains=str(tj)) | Q(domain_name__contains=str(tj)) | Q(domain_remark__contains=str(tj)))
                total = rearch_data.count()
                data="{\"rows\":"+json.dumps(list(rearch_data.values()))+",\"total\":\""+str(total)+"\",\"record_line\":"+json.dumps(list(record_line))+"}"
                #domain查找
                logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(tj))
                return HttpResponse(data)

        elif action == 'editFun':#增加和删除，依据域名ID的唯一性
            domain_id = request.POST.get('domain_id', '').encode('latin-1', 'ignore').strip()
            domain_status = request.POST.get('domain_status', '').encode('latin-1', 'ignore').strip()
            domain_name = request.POST.get('domain_name', '').encode('latin-1', 'ignore').strip()
            domain_records = request.POST.get('domain_records', '').encode('latin-1', 'ignore').strip()
            domain_remark = request.POST.get('domain_remark', '')

            domain_dict = {'domain_id':domain_id,
                        'domain_status':domain_status,
                        'domain_name':domain_name,
                        'domain_records':domain_records,
                        'domain_remark':domain_remark,}

            DomainUpdate = models.DomainInfo.objects.filter(domain_id=domain_id)
            #login_token=16080,94a8f63fc836d76ceb76ab4cdb36ee78
            try:
                if DomainUpdate:
                    CMD ="curl -sX POST https://dnsapi.cn/Domain.Remark -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id="+domain_id+"&remark="+domain_remark+"'"
                    raw_data=commands.getoutput(CMD)
                    req=json.loads(raw_data)
                    if req['status']['code'] == '1':
                    # CMD ="curl -sX POST https://dnsapi.cn/Domain.Remark -d 'login_token=LOGIN_TOKEN&format=json&domain_id=domain_id&remark=domain_remark'"
                        # pass
                        DomainUpdate.update(**domain_dict)
                        detail ='更新:'
                        for i in domain_dict:detail+=i+":"+domain_dict[i]+";"
                        logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(detail))
                    else:
                        return HttpResponse(req['status']['message'])
                    # DomainUpdate.update(**domain_dict)
                else:
                    pass
                    # models.DomainInfo.objects.create(**domain_dict)
            except :return HttpResponse('0')
            else:return HttpResponse('1')

        elif action == 'deleteFun':
            id = request.POST.get('id','').encode('latin-1', 'ignore').strip().split(',')
            '''
            删除单条domain信息
            CMD ="curl -sX POST https://dnsapi.cn/Domain.Remove -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id="+domain_id+"'"
            '''
            try:
                for i in range(len(id)):
                    models.DomainInfo.objects.get(id=id[i]).delete()
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(id[i]))
            except Exception, e:
                pass
            else:
                return HttpResponse('1')

        else:return HttpResponse(x_message)
    elif dbname == 'dnsinfo':
        if action == 'pagedataList':
            # return HttpResponse(base_id)

            #此时的dns_id=domian_id
            tj=Vre(request.POST.get('tj', ''))
            page=int(request.POST.get('page', '1').encode('latin-1', 'ignore').strip())
            num=int(request.POST.get('num', '15').encode('latin-1', 'ignore').strip())

            if base_id =='':domain_data=models.DnsInfo.objects.values()[(page-1)*num:page*num]
            else:domain_data = models.DnsInfo.objects.filter(Domain_name_id=base_id).values()[(page-1)*num:page*num]
            # else:domain_data=models.DnsInfo.objects.values()[(page-1)*num:page*num]

            #获取所有的domain的列表
            domainlist = models.DomainInfo.objects.values()

            #查找数据
            if tj=="":
                total = models.DnsInfo.objects.count()
                data="{\"rows\":"+json.dumps(list(domain_data))+",\"total\":\""+str(total)+"\",\"domainlist\":"+json.dumps(list(domainlist))+"}"
                return HttpResponse(data)
            else:
                rearch_data = models.DnsInfo.objects.filter(
                    Q(dns_id__contains=str(tj)) | Q(dns_name__contains=str(tj)) | Q(dns_value__contains=str(tj)) | Q(dns_remark__contains=str(tj)) \
                    | Q(dnsop__contains=str(tj)))
                total = rearch_data.count()
                data="{\"rows\":"+json.dumps(list(rearch_data.values()))+",\"total\":\""+str(total)+"\",\"domainlist\":"+json.dumps(list(domainlist))+"}"
                logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(tj))
                return HttpResponse(data)

        elif action == 'editFun':

            record_id = request.POST.get('dns_id', '')
            
            remark = request.POST.get('dns_remark', '')
            dns_dict = {'dns_id':request.POST.get('dns_id', ''),
                        'dns_name':request.POST.get('dns_name', ''),
                        'dns_type':request.POST.get('dns_type', ''),
                        'dns_line':request.POST.get('dns_line', ''),
                        'dns_value':request.POST.get('dns_value', ''),
                        'dns_weight':request.POST.get('dns_weight', ''),
                        'dns_mx':request.POST.get('dns_mx', ''),
                        'dns_ttl':request.POST.get('dns_ttl', ''),
                        'dns_enabled':request.POST.get('dns_enabled', ''),
                        'dns_updated_on':request.POST.get('dns_updated_on', ''),
                        'dnsop':request.POST.get('dnsop', ''),
                        'dns_remark':request.POST.get('dns_remark', ''),
                        'Domain_name_id':request.POST.get('Domain_name_id', ''),
                        }


            DnsUpdate_dnsid = models.DnsInfo.objects.filter(dns_id=dns_dict['dns_id'])
            DnsUpdate_Domainid = models.DomainInfo.objects.filter(id=dns_dict['Domain_name_id'])

            domain_id = models.DomainInfo.objects.get(id=dns_dict['Domain_name_id']).domain_id

            try:
                if DnsUpdate_dnsid:
                    if DnsUpdate_Domainid:#如果dns记录与父记录（domain）都存在，即代表dns数据存在，更新即可
                        # 已测试，status: 系统内部标识状态, 开发者可忽略
                        # 内容line、type、记录值之间存在很多约束关系，API无法体现，需要额外制定操作规范
                        '''
                        update_CMD = "curl -sX POST https://dnsapi.cn/Record.Modify -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id="+domain_id+"&record_id="+record_id+"\
                        &sub_domain="+dns_dict['dns_name']+"&value="+dns_dict['dns_value']+"&record_type="+dns_dict['dns_type']+"\
                        &record_line_id="+dns_dict['dns_line'].replace("=","%3D")+"&ttl ="+dns_dict['dns_ttl']+"'"

                        #"&weight ="+dns_dict['dns_weight']+"&mx ="+dns_dict['dns_mx']+"&ttl ="+dns_dict['dns_ttl']+
                        raw_data=commands.getoutput(update_CMD)
                        req=json.loads(raw_data)
                        if req['status']['code'] == '1':
                            return HttpResponse('修改成功')
                        else:
                            return HttpResponse(req['status']['code']+":"+req['status']['message'])
                        '''

                        # 测试uodate_CMD时注销
                        #更新dns备注信息
                        CMD ="curl -sX POST https://dnsapi.cn/Record.Remark -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id="+domain_id+"&record_id="+record_id+"&remark="+remark+"'"
                        raw_data=commands.getoutput(CMD)
                        req=json.loads(raw_data)
                        # return HttpResponse(req['status']['code'])
                        if req['status']['code'] == '1':
                            DnsUpdate_dnsid.update(**dns_dict)
                        detail ='更新:'
                        for i in dns_dict:detail+=i+":"+dns_dict[i]+";"
                        logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(detail))

                        '''
                        #更新dns的状态，启用或者停止
                        CMD ="curl -sX POST https://dnsapi.cn/Record.Status  -d \
                        'login_token="+LOGIN_TOKEN+"&format=json&\
                        domain_id="+Domain_name_id+"&\
                        record_id="+dns_id+"&\
                        status="+dns_enabled+"'"
                        raw_data=commands.getoutput(CMD)
                        req=json.loads(raw_data)
                        if req['status']['code'] == '1':
                            DomainUpdate.update(**domain_dict)
                        '''

                    else:return HttpResponse('域名不存在,请选择正确的域名信息')
                else:
                    if DnsUpdate_Domainid:#如果dns id不存在，但是domain）存在，创建数据
                        models.DnsInfo.objects.create(**dns_dict)
                    else:return HttpResponse('域名不存在,请选择正确的域名信息')
            except Exception as e :return HttpResponse(e)
            else:return HttpResponse('1')

        elif action == 'deleteFun':
            id = request.POST.get('id','').encode('latin-1', 'ignore').strip().split(',')

            '''
            # 删除record记录,待测试
            for i in range(len(id)):
                record_obj=models.DnsInfo.objects.get(id=id[i])
                # domain_id=models.DomainInfo.objects.get(id=record_obj.Domain_name_id).domain_id
                domain_id=models.DnsInfo.objects.filter(Domain_name__id=id).domain_id
                return HttpResponse('断点1')

                del_CMD ="curl -sX POST https://dnsapi.cn/Record.Remove  -d 'login_token="+LOGIN_TOKEN+"&format=json&domain_id="+domain_id+"&record_id="+record_obj.dns_id+"'"
                raw_data=commands.getoutput(CMD)
                req=json.loads(raw_data)
                undel_list=""
                if req['status']['code'] == '1':
                    models.DnsInfo.objects.get(dns_id=record_id).delete()
                    # return HttpResponse('删除成功')
                else:
                    undel_list+=record_id.dns_id+','
                    # return HttpResponse('ID:'+record_id+'未被删除;'+req['status']['code']+":"+req['status']['message'])
            if undel_list =="":pass
            else:return HttpResponse('ID:'+str(undel_list)+'未被删除')
            '''
            
            # 测试del_CMD时注释
            
            try:
                for i in range(len(id)):
                    models.DnsInfo.objects.get(id=id[i]).delete()
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str('id='+id[i]))
            except Exception, e:
                pass
            else:
                return HttpResponse('1')
            
        else:return HttpResponse(x_message)



    else:return HttpResponse(x_message)

data_dict = {
    'baseinfo':
        {'tablesname':models.BaseInfo,'field':['sid','hostname','isp','status','create_date','expire_date','admin','business_unit','tags','memo',]},
    'configinfo':
        {'tablesname':models.ConfigInfo,'field':['baseid','cpu_info','men_info','disk_info','os','public_ip','private_ip','mgmt_ip',]},
    'businessinfo':
        {'tablesname':models.BusinessUnit,'field':['name','admin','memo',]},
    'platforminfo':
        {'tablesname':models.Platform,'field':['name','domain','url','phonecall','memo',]},
    'domaininfo':
        {'tablesname':models.DomainInfo,'field':['domain_id','domain_status','domain_name','domain_records','domain_remark',]},
    'dnsinfo':
        {'tablesname':models.DnsInfo,'field':['Domain_name','dns_id','dns_name','dns_type','dns_line','dns_value','dns_weight',\
        'dns_mx','dns_ttl','dns_enabled','dns_remark','dns_updated_on','dnsop',]},
}

@check_permission
@login_required
@require_POST
# @permission_required('add_contenttype')
def base_data(request):
    # return HttpResponse(request.get_full_path())

    x_message=request.session.get('x_message',"您的请求已被拦截05！")
    if len(request.get_full_path().lstrip('/').strip().split('/')[1].split('_')) < 2:
        return HttpResponse(x_message)
    dbname=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[0]
    #dbname可能等于domaininfo,dnsinfo两种，后续还会加上baseinfo，configinfo等
    action=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[1]
    #action可能等于pagedataList,editFun,deleteFun,sync四种,即增删改查与同步
    tj=Vre(request.POST.get('tj', ''))
    page=int(request.POST.get('page', '1').encode('latin-1', 'ignore').strip())
    num=int(request.POST.get('num', '10').encode('latin-1', 'ignore').strip())

    V=request.get_full_path().lstrip('/').strip()
    try:
        config_id=V.split('.')[1].split('?')[1].split('=')[1]
    except:
        config_id=''

    if data_dict.has_key(dbname):
        tablename = data_dict[dbname]['tablesname']
        if action == 'pagedataList':#执行所有表的查询
            result_data = tablename.objects.values().order_by('-id')[(page-1)*num:page*num]
            platformlist = models.Platform.objects.values()#云平台列表
            businessunitlist = models.BusinessUnit.objects.values()#业务线列表
            baseinfolist = models.BaseInfo.objects.values()#云资源列表
            if tj == '':
                if dbname == 'baseinfo':
                    result_data = models.BaseInfo.objects.values().order_by('expire_date')[(page-1)*num:page*num]
                    for item in result_data:
                        PlatformQueset= models.Platform.objects.filter(id=item['isp_id'])
                        for Platname in PlatformQueset:item['isp'] = Platname.name
                        #根据baseinfo表中id号去关联关系中取对应的业务线
                        base_obj = models.BaseInfo.objects.get(id=item['id'])
                        #base_obj.business_unit.all()
                        businessline=""
                        for line in base_obj.business_unit.all():businessline+=line.name+','
                        item['business_unit'] = businessline
                        item['sid'] = '<a href="/info/hostconfig.html?config_id='+str(item['id'])+'">'+item['sid']+'</a>'
                        curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
                        curr_date = datetime.datetime.strptime(curr_date_str,'%Y-%m-%d %H:%M:%S')#将当前时间转换成可加减的日期格式
                        one_mouth_later = curr_date + datetime.timedelta(days=30)
                        one_mouth_later_str = one_mouth_later.strftime('%Y-%m-%d %H:%M:%S')
                        # one_hour_before = curr_date + datetime.timedelta(hours=hours)
                        # one_hour_before_str = one_hour_before.strftime('%Y-%m-%d %H:%M:%S')
                        if str(item['expire_date']) < curr_date_str:
                            item['expire_date'] = '<a style="color:red">'+str(item['expire_date']).split('+')[0]+'</a>'
                            # item['memo'] = '<a style="color:red">'+'已到期，请及时续费'+'</a>'
                        elif str(item['expire_date']) > curr_date_str and str(item['expire_date']) < one_mouth_later_str:
                            item['expire_date'] = '<a style="color:blue">'+str(item['expire_date']).split('+')[0]+'</a>'
                            # item['memo'] = '<a style="color:blue">'+'即将到期，请及时续费'+'</a>'                            
                elif dbname == 'configinfo':
                    V=request.get_full_path().lstrip('/').strip()
                    try:
                        config_id=V.split('.')[1].split('?')[1].split('=')[1]
                    except:
                        config_id=''

                    #获取url中id=值，如果存在，则修改后停留当前url，如果不存在，则代表选择全局页面编辑，停留在全局页面
                    try:
                        if base_id:result_data=tablename.objects.filter(baseid_id=base_id).values().order_by('-id')[(page-1)*num:page*num]
                        else:result_data=tablename.objects.values().order_by('-id')[(page-1)*num:page*num]
                    except :
                        result_data=tablename.objects.values().order_by('-id')[(page-1)*num:page*num]
                    else:
                        pass

                    for item in result_data:
                        BaseQueset = models.BaseInfo.objects.filter(id=item['baseid_id'])
                        for basename in BaseQueset:item['baseid_id'] = basename.sid
                    # return HttpResponse('测试断点02')
                else:pass
                total = tablename.objects.count()
                data="{\"rows\":"+json.dumps(list(result_data),cls=CJsonEncoder)+",\"total\":\""+str(total)+"\",\"platformlist\":" \
                +json.dumps(list(platformlist),cls=CJsonEncoder)+",\"businessunitlist\":"+json.dumps(list(businessunitlist),cls=CJsonEncoder)+",\"baseinfolist\":" \
                +json.dumps(list(baseinfolist),cls=CJsonEncoder)+"}"
            else:
                if dbname == 'baseinfo':
                    rearch_data = models.BaseInfo.objects.filter(Q(sid__contains=str(tj)) |Q(hostname__contains=str(tj)) |Q(isp__name__contains=str(tj)) \
                        | Q(status__contains=str(tj)) | Q(admin__contains=str(tj)) | Q(business_unit__name__contains=str(tj)) | Q(tags__contains=str(tj))\
                        | Q(memo__contains=str(tj))).values().order_by('expire_date').distinct()

                    for item in rearch_data:
                        PlatformQueset= models.Platform.objects.filter(id=item['isp_id'])
                        for Platname in PlatformQueset:item['isp'] = Platname.name
                        # 根据baseinfo表中id号去关联关系中取对应的业务线
                        base_obj = models.BaseInfo.objects.get(id=item['id'])
                        # base_obj.business_unit.all()

                        businessline=""
                        for line in base_obj.business_unit.all():businessline+=line.name+','

                        item['business_unit'] = str(businessline)
                        item['sid'] = '<a href="/info/hostconfig.html?config_id='+str(item['id'])+'">'+item['sid']+'</a>'
                        curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
                        curr_date = datetime.datetime.strptime(curr_date_str,'%Y-%m-%d %H:%M:%S')#将当前时间转换成可加减的日期格式
                        one_mouth_later = curr_date + datetime.timedelta(days=30)
                        one_mouth_later_str = one_mouth_later.strftime('%Y-%m-%d %H:%M:%S')
                        # one_hour_before = curr_date + datetime.timedelta(hours=hours)
                        # one_hour_before_str = one_hour_before.strftime('%Y-%m-%d %H:%M:%S')
                        if str(item['expire_date']) < curr_date_str:
                            item['expire_date'] = '<a style="color:red">'+str(item['expire_date']).split('+')[0]+'</a>'
                            item['memo'] = '<a style="color:red">'+'已到期，请及时续费'+'</a>'
                        elif str(item['expire_date']) > curr_date_str and str(item['expire_date']) < one_mouth_later_str:
                            item['expire_date'] = '<a style="color:blue">'+str(item['expire_date']).split('+')[0]+'</a>'
                            item['memo'] = '<a style="color:blue">'+'即将到期，请及时续费'+'</a>' 
                elif dbname == 'configinfo':
                    rearch_data = models.ConfigInfo.objects.filter(Q(baseid__sid__contains=str(tj)) | Q(cpu_info__contains=str(tj)) \
                        | Q(men_info__contains=str(tj)) | Q(disk_info__contains=str(tj)) | Q(os__contains=str(tj)) \
                        | Q(public_ip__contains=str(tj))| Q(private_ip__contains=str(tj))| Q(mgmt_ip__contains=str(tj)) \
                        | Q(memo__contains=str(tj))).values().order_by('-id')

                    try:
                        if base_id:result_data=tablename.objects.filter(baseid_id=base_id).values().order_by('-id')[(page-1)*num:page*num]
                        else:result_data=tablename.objects.values().order_by('-id')[(page-1)*num:page*num]
                    except :
                        result_data=tablename.objects.values().order_by('-id')[(page-1)*num:page*num]
                    else:
                        pass

                    for item in rearch_data:
                        BaseQueset = models.BaseInfo.objects.filter(id=item['baseid_id'])
                        for basename in BaseQueset:item['baseid_id'] = basename.sid

                elif dbname == 'platforminfo':
                    rearch_data = tablename.objects.filter(Q(name__contains=str(tj)) | Q(domain__contains=str(tj)) | Q(url__contains=str(tj)) \
                        | Q(phonecall__contains=str(tj))| Q(memo__contains=str(tj))).values().order_by('-id')
                elif dbname == 'businessinfo':
                    rearch_data = tablename.objects.filter(Q(name__contains=str(tj)) | Q(admin__contains=str(tj))| Q(memo__contains=str(tj))).values().order_by('-id')
                total = rearch_data.count()
                data="{\"rows\":"+json.dumps(list(rearch_data[(page-1)*num:page*num]),cls=CJsonEncoder)+",\"total\":\""+str(total)+"\"}"
                logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(tj))
            return HttpResponse(data)

        elif action == 'editFun':#执行所有的编辑与修改
            # return HttpResponse(request.get_full_path())
            #平台配置新增与修改
            if dbname == 'platforminfo':
                name = request.POST.get('name', '')
                domain = request.POST.get('domain', '')
                url = request.POST.get('url', '')
                phonecall = request.POST.get('phonecall', '')
                memo = request.POST.get('memo', '')

                plat_dict = {'name':name,'domain':domain,'url':url,'phonecall':phonecall,'memo':memo,}

                PlatUpdate = models.Platform.objects.filter(name=name)
                try:
                    if PlatUpdate:
                        PlatUpdate.update(**plat_dict)
                        detail ='更新:'
                        act_type='update'
                    else:
                        models.Platform.objects.create(**plat_dict)
                        detail ='创建:'
                        act_type='create'
                    for i in plat_dict:detail+=i+":"+plat_dict[i]+";"
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=act_type,act_detail=str(detail))
                except Exception as e :return HttpResponse(e)
                else:return HttpResponse('1')

            #执行业务线新增与修改
            elif dbname == 'businessinfo':
                name = request.POST.get('name', '')
                admin = request.POST.get('admin', '')
                memo = request.POST.get('memo', '')

                business_dict = {'name':name,'admin':admin,'memo':memo,}

                BusinessUpdate = models.BusinessUnit.objects.filter(name=name)
                try:
                    if BusinessUpdate:
                        BusinessUpdate.update(**business_dict)
                        detail ='更新:'
                        act_type='update'
                    else:
                        models.BusinessUnit.objects.create(**business_dict)
                        detail ='创建:'
                        act_type='create'
                    for i in business_dict:detail+=i+":"+business_dict[i]+";"
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=act_type,act_detail=str(detail))
                except Exception as e :return HttpResponse(e)
                else:return HttpResponse('1')

            #执行云资源新增与修改
            elif dbname == 'baseinfo':
                sid = request.POST.get('sid', '')
                hostname = request.POST.get('hostname', '')
                isp = request.POST.get('isp_id', '').encode('latin-1', 'ignore').strip()
                status = request.POST.get('status', '')
                create_date = request.POST.get('create_date', '')
                expire_date = request.POST.get('expire_date', '')
                admin = request.POST.get('admin', '')
                business_unit = request.POST.get('business_unit', '').encode('latin-1', 'ignore').strip().split(',')
                tags = request.POST.get('tags', '')
                memo = request.POST.get('memo', '')

                isp_choice = models.Platform.objects.get(id=int(isp))

                base_dict = {'sid':sid,'hostname':hostname,'isp':isp_choice,'status':status,'create_date':create_date,'expire_date':expire_date,\
                'admin':admin,'tags':tags,'memo':memo,}

                baseinfoUpdate = models.BaseInfo.objects.filter(sid=sid)

                try:
                    if baseinfoUpdate:
                        baseinfoUpdate.update(**base_dict)
                        # detail ='更新:'
                        act_type='update'
                    else:
                        #创建不含多对多的记录
                        models.BaseInfo.objects.create(**base_dict)
                        # detail ='创建:'
                        act_type='create'
                    # for i in base_dict:detail+=i+":"+base_dict[i]+";"
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=act_type,act_detail=str(base_dict))

                    #业务线修改通过先删除，后新增的方式实现
                    base_obj =models.BaseInfo.objects.get(sid=base_dict['sid'])#获取该记录
                    bussiness_obj_del = models.BusinessUnit.objects.all()
                    base_obj.business_unit.remove(*bussiness_obj_del)
                    for i in range(len(business_unit)):
                        bussid = business_unit[i]
                        bussiness_obj = models.BusinessUnit.objects.filter(id=bussid)#获取业务线queryset
                        base_obj.business_unit.add(*bussiness_obj)#关联该对象

                except Exception as e :return HttpResponse(e)
                else:return HttpResponse('1')
                # else:return HttpResponse('request.get_full_path()')

            #执行配置信息新增与修改
            elif dbname == 'configinfo':
                baseid = request.POST.get('baseid_id', '').encode('latin-1', 'ignore').strip()
                cpu_info = request.POST.get('cpu_info', '')
                men_info = request.POST.get('men_info', '')
                disk_info = request.POST.get('disk_info', '')
                os = request.POST.get('os', '')
                public_ip = request.POST.get('public_ip', '')
                private_ip = request.POST.get('private_ip', '')
                mgmt_ip = request.POST.get('mgmt_ip', '')
                memo = request.POST.get('memo', '')

                base_choice = models.BaseInfo.objects.get(id=int(baseid))

                config_dict = {'baseid':base_choice,'cpu_info':cpu_info,'men_info':men_info,\
                'disk_info':disk_info,'os':os,'public_ip':public_ip,\
                'private_ip':private_ip,'mgmt_ip':mgmt_ip,'memo':memo}

                # ConfigUpdate = models.ConfigInfo.objects.filter(baseid=baseid,public_ip=public_ip,private_ip=private_ip)
                ConfigUpdate = models.ConfigInfo.objects.filter(private_ip=private_ip)
                try:
                    if ConfigUpdate:
                        ConfigUpdate.update(**config_dict)
                        # detail = "更新"
                        act_type='update'
                    else:
                        models.ConfigInfo.objects.create(**config_dict)
                        # detail = "创建"
                        act_type='create'
                    # for i in config_dict:detail+=i+":"+config_dict[i]+";"
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=act_type,act_detail=str(config_dict))
                except Exception as e :return HttpResponse(e)
                else:return HttpResponse('1')
            else:pass

        elif action == 'deleteFun':#执行所有的删除
            id = request.POST.get('id','').encode('latin-1', 'ignore').strip().split(',')
            try:
                for i in range(len(id)):
                    tablename.objects.get(id=id[i]).delete()
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str('id='+id[i]))
            except Exception, e:
                pass
            else:
                return HttpResponse('1')

    else:pass

@check_permission
@login_required
@require_POST
def asset_data(request):
    x_message=request.session.get('x_message',"您的请求已被拦截05！")
    if len(request.get_full_path().lstrip('/').strip().split('/')[1].split('_')) < 2:
        return HttpResponse(x_message)
    dbname=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[0]
    action=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[1]

    if dbname == 'assetinfo':
        if action == 'pagedataList':
            tj=Vre(request.POST.get('tj', ''))

            # return HttpResponse(request.get_full_path())
            page=int(request.POST.get('page', '1').encode('latin-1', 'ignore').strip())
            num=int(request.POST.get('num', '10').encode('latin-1', 'ignore').strip())
            if tj=="":
                asset_data=models.Asset.objects
                # total = models.Asset.objects.all().count()
            else:
                asset_data=models.Asset.objects.filter(
                    Q(device_id__contains=str(tj)) | Q(device_type__contains=str(tj)) | Q(device_model__contains=str(tj)) \
                    | Q(device_status__contains=str(tj)) | Q(device_dept__contains=str(tj)) | Q(device_user__contains=str(tj))\
                    | Q(device_memo__contains=str(tj)))
                logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(tj))
            total = asset_data.count()
            data="{\"rows\":"+json.dumps(list(asset_data.values().order_by('-id')[(page-1)*num:page*num]))+",\"total\":\""+str(total)+"\"}"
            return HttpResponse(data)

        elif action == 'editFun':#增加和删除，依据域名ID的唯一性
            paramlist =['device_id','device_type','device_model','device_status','device_dept','device_user','device_memo']
            paramdict ={}
            for paramobj in paramlist:
                param_value = request.POST.get(str(paramobj),'').strip()
                paramdict[paramobj] = param_value

            AssetUpdate = models.Asset.objects.filter(device_id=paramdict['device_id'])

            try:
                if AssetUpdate:
                    AssetUpdate.update(**paramdict)
                    detail ='更新:'
                    act_type='update'
                else:
                    models.Asset.objects.create(**paramdict)
                    detail ='创建:'
                    act_type='create'
                for i in paramdict:detail+=i+":"+paramdict[i]+";"
                logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=act_type,act_detail=str(detail))

            except :return HttpResponse('0')
            else:return HttpResponse('1')
            # pass

        elif action == 'deleteFun':
            id = request.POST.get('id','').encode('latin-1', 'ignore').strip().split(',')
            try:
                for i in range(len(id)):
                    models.Asset.objects.get(id=id[i]).delete()
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str('id='+id[i]))
            except Exception, e:
                pass
            else:
                return HttpResponse('1')




def AlertDataInquery(curr_date,curr_date_str,hours=-2):
    #告警数据
    one_hour_before = curr_date + datetime.timedelta(hours=hours)
    one_hour_before_str = one_hour_before.strftime('%Y-%m-%d %H:%M:%S')
    one_hour_ok = models.ZabbixAlertInfo.objects.filter(Q(alerttime__gte=one_hour_before_str) & Q(alerttime__lte=curr_date_str)).filter(status="OK").count()
    one_hour_problem = models.ZabbixAlertInfo.objects.filter(Q(alerttime__gte=one_hour_before_str) & Q(alerttime__lte=curr_date_str)).filter(status="PROBLEM").count()

    return one_hour_ok,one_hour_problem




@check_permission
@login_required
# @permission_required('add_contenttype')
def alarm_data(request):
    x_message=request.session.get('x_message',"您的请求已被拦截05！")
    if len(request.get_full_path().lstrip('/').strip().split('/')[1].split('_')) < 2:
        return HttpResponse(x_message)
    dbname=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[0]
    action=request.get_full_path().lstrip('/').strip().split('/')[1].split('_')[1]
    
    if dbname == 'alarminfo':
        # domain_data=models.ZabbixAlertInfo.objects.values().order_by('-id')[(page-1)*num:page*num]
        curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
        curr_date = datetime.datetime.strptime(curr_date_str,'%Y-%m-%d %H:%M:%S')#将当前时间转换成可加减的日期格式
        if action == 'pagedataList':
            tj=Vre(request.POST.get('tj', ''))

            # return HttpResponse(request.get_full_path())
            page=int(request.POST.get('page', '1').encode('latin-1', 'ignore').strip())
            num=int(request.POST.get('num', '10').encode('latin-1', 'ignore').strip())
            
            alarm_problem = models.ZabbixAlertInfo.objects.filter(status="PROBLEM").values()

            alarm_data=models.ZabbixAlertInfo.objects.values().order_by('-id')[(page-1)*num:page*num]



            if tj=="":
                total = models.ZabbixAlertInfo.objects.count()
                data="{\"rows\":"+json.dumps(list(alarm_data))+",\"total\":\""+str(total)+"\",\"alarm_problem\":"+json.dumps(list(alarm_problem))+"}"
                # data="{\"rows\":"+json.dumps(list(alarm_data))+",\"total\":\""+str(total)+"\"}"
                return HttpResponse(data)
            else:
                rearch_data = models.ZabbixAlertInfo.objects.filter(
                    Q(eventid__contains=str(tj)) | Q(alerttime__contains=str(tj)) | Q(subject__contains=str(tj)) \
                    | Q(message__contains=str(tj))| Q(sendto__contains=str(tj))| Q(status__contains=str(tj)))
                total = rearch_data.count()
                data="{\"rows\":"+json.dumps(list(rearch_data.values().order_by('-id')[(page-1)*num:page*num]))+",\"total\":\""+str(total)+"\",\"alarm_problem\":"+json.dumps(list(alarm_problem))+"}"
                # data="{\"rows\":"+json.dumps(list(rearch_data.values().order_by('-id')[(page-1)*num:page*num]))+",\"total\":\""+str(total)+"\"}"
                logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str(tj))
                return HttpResponse(data)
        elif action == 'getalert':
            one_hour_ok,one_hour_problem = AlertDataInquery(curr_date,curr_date_str)
            data="{\"today_ok_total\":\""+str(one_hour_ok)+"\",\"today_problem_total\":\""+str(one_hour_problem)+"\"}"
            return HttpResponse(data)
        elif action == "charts":  
            one_hour_ok,one_hour_problem = AlertDataInquery(curr_date,curr_date_str)
            #画图数据
            check_date=request.POST.get('text', '')
            before_day = curr_date + datetime.timedelta(hours=-int(check_date))
            before_day_str = before_day.strftime('%Y-%m-%d %H:%M:%S')#字符串
            day_count = []
            while before_day_str < curr_date_str:
                before_day+=datetime.timedelta(hours=1)
                before_day_str = before_day.strftime('%Y-%m-%d %H:%M:%S')
                time_re_str = before_day_str.split(":")[0]
                count_detail={}
                count_detail['DATE'] =time_re_str +':00:00'
                count_detail['COUNT'] =models.ZabbixAlertInfo.objects.filter(alerttime__contains=time_re_str).count()
                count_detail['OK'] =models.ZabbixAlertInfo.objects.filter(alerttime__contains=time_re_str).filter(status="OK").count()
                count_detail['PROBLEM'] =count_detail['COUNT']-count_detail['OK']
                day_count.append(count_detail)
            
            alarm_problem = models.ZabbixAlertInfo.objects.filter(status="PROBLEM").values()
            alarm_ok = models.ZabbixAlertInfo.objects.filter(status="OK").values()
            # data="{\"rows\":"+json.dumps(list(alarm_data))+",\"alarm_problem\":"+json.dumps(list(alarm_problem))+",\"alarm_ok\":"+json.dumps(list(alarm_ok))+"}"
            data="{\"alarm_problem\":"+json.dumps(list(alarm_problem))+",\"alarm_ok\":"+json.dumps(list(alarm_ok))+",\"day_count\":"+json.dumps(day_count)+",\
            \"today_ok_total\":\""+str(one_hour_ok)+"\",\"today_problem_total\":\""+str(one_hour_problem)+"\"}"
            return HttpResponse(data)
        elif action =='deleteFun':
            id = request.POST.get('id','').encode('latin-1', 'ignore').strip().split(',')
            try:
                for i in range(len(id)):
                    models.ZabbixAlertInfo.objects.get(id=id[i]).delete()
                    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type=action,act_detail=str('id='+id[i]))
            except Exception, e:
                pass
            else:
                return HttpResponse('1')


class TestView(TemplateView):
    template_name = 'test.html'


@check_permission
@login_required
def auth_data(request):
    # request_url = request.get_full_path().split('/')
    options = request.get_full_path().split('/')[2]
    # options_obj = request_url[3]
    if request.method =='POST':
        #request.get_full_path() = /url/动作/
        #动作里面含数据
        if options == 'useradd':
            # userinfolist =['username','password','first_name','email','usrpermissionlist','groupslist','is_active','is_staff','is_superuser']
            userinfolist =['username','password','first_name','email','is_active','is_staff','is_superuser']
            dict01 ={}
            for userobj in userinfolist:
                userinfo_key = request.POST.get(str(userobj),'').encode('latin-1', 'ignore').strip()
                dict01[userobj] = userinfo_key
                if userinfo_key == 'True':
                    dict01[userobj] = True
                elif userinfo_key == 'False':
                    dict01[userobj] = False
                else:pass            
            userupdate = User.objects.filter(username=dict01['username'])
            if userupdate:ret='0'
            else:
                User.objects.create(**dict01)
                user_obj=User.objects.get(username=dict01['username'])#得到user对象
                
                # usrpermissionlist = request.POST.get('usrpermissionlist','').encode('latin-1', 'ignore').strip().split(',')
                # groupslist = request.POST.get('groupslist','').encode('latin-1', 'ignore').strip().split(',')
                
                usrpermissionlist = request.POST.get('usrpermissionlist','').split(',')
                groupslist = request.POST.get('groupslist','').split(',')



                # 多对多添加用户属组
                for grp in groupslist:
                    group_obj = Group.objects.get(name=str(grp))#根据name获取Group对象
                    user_obj.groups.add(group_obj)
                '''用户的权限=(用户属组1的权限+用户属组2的权限+....+用户的权限).去重'''
                    
                
                #多对多添加用户权限
                for usr in usrpermissionlist:
                    # perm_obj = Permission.objects.get(name=str(li.split(" | ")[0]))#根据name获取Permission对象
                    perm_obj = Permission.objects.get(name=str(usr))#根据name获取Permission对象
                    user_obj.user_permissions.add(perm_obj)


                user_obj.set_password(dict01['password'])
                user_obj.is_active =(dict01['is_active'])
                user_obj.is_staff =(dict01['is_staff'])
                user_obj.is_superuser =(dict01['is_superuser'])


                user_obj.save()
                ret='1'

            return HttpResponse(ret)

        elif options == 'groupsadd':

            # groupname = request.POST.get('groupname','').encode('latin-1', 'ignore').strip()
            groupname = request.POST.get('groupname','')

            groupsupdate = Group.objects.filter(name=groupname)
            if groupsupdate:ret='0'
            else:
                group_obj = Group.objects.create(name=groupname)
                # grouppermissionlist = request.POST.get('grouppermissionlist','').encode('latin-1', 'ignore').strip().split(',')
                grouppermissionlist = request.POST.get('grouppermissionlist','').split(',')
                for li in grouppermissionlist:
                    perm_obj = Permission.objects.get(name=str(li.split(" | ")[0]))#根据name获取Permission对象
                    group_obj.permissions.add(perm_obj)
                ret ='1'
            return HttpResponse(ret)

        elif options == 'get_groupslist_and_permission':
            #以Permission表中的name字段进行返回
            all_permissions = Permission.objects.all().values()
            all_permissionslist = [i['name'] for i in all_permissions]


            all_groupslist =[]        
            grouplist_obj = Group.objects.all()
            for item in grouplist_obj:all_groupslist.append(item.name)

            all_user = User.objects.all().values()
            all_userlist = [i['username'] for i in all_user]

            data = "{\"all_permissionslist\":"+json.dumps(all_permissionslist)+",\"all_groupslist\":"+json.dumps(all_groupslist)+",\"all_userlist\":"+json.dumps(all_userlist)+"}"
            return HttpResponse(data)
        elif options == 'userinfolist':
            tj=Vre(request.POST.get('tj', ''))
            page = int(request.POST.get('page','1').encode('latin-1', 'ignore').strip())
            num = int(request.POST.get('num','15').encode('latin-1', 'ignore').strip())
            if tj=="":
                userlist = User.objects.values().order_by('-id')[(page-1)*num:page*num]
            else:
                userlist = User.objects.filter(Q(username__contains=str(tj)) | Q(email__contains=str(tj)) | Q(first_name__contains=str(tj)))\
                .values().order_by('-id')[(page-1)*num:page*num]
            for item in userlist:
                if item['is_active']:item['is_active'] ='是'
                else:item['is_active'] = '否'                
                if item['is_staff']:item['is_staff'] ='是'
                else:item['is_staff'] = '否'                
                if item['is_superuser']:
                    item['is_superuser'] ='是'
                    item['get_all_permissions'] = '具备所有权限'
                else:
                    item['is_superuser'] = '否'
                    # item['get_all_permissions'] = str([ i for i in User.objects.get(username=item['username']).get_all_permissions()])
                    permission_str = "-"
                    # permission_list=[i for i in User.objects.get(username=item['username']).get_all_permissions()]
                    permission_list=[i for i in User.objects.get(username=item['username']).user_permissions.all()]
                    for items in range(len(permission_list)):
                        # if settings['Matrix'].has_key(permission_list[items].split('.')[1]):
                        if settings['Matrix'].has_key(permission_list[items].codename):
                            # permission_list[items] +=' | '+ settings['Matrix'][permission_list[items].split('.')[1]]
                            permission_str += settings['Matrix'][permission_list[items].codename].encode("utf8")+','
                    # item['get_all_permissions'] = str(permission_list)
                    '''
                    用户的权限=(用户属组1的权限+用户属组2的权限+....+用户的权限).去重
                    '''
                    # user_groupslist = [i for i in User.objects.get(username=item['username'])]
                    # aa = User.objects.get(username=item['username'])
                    # bb = aa.groups.all()
                    # for j in [i for i in User.objects.get(username=item['username']).groups.all()]:print j.name

                    item['get_all_permissions'] = permission_str

                groupsSet = Group.objects.filter(user__username=item['username'])
                
                if groupsSet == []:
                    item['groups'] = "无属组"
                else:
                    grouplist = []
                    for groupitem in groupsSet:
                        grouplist.append(str(groupitem.name))
                    item['groups'] = str(grouplist)

            total = userlist.count()
            data="{\"rows\":"+json.dumps(list(userlist),cls=CJsonEncoder)+",\"total\":\""+str(total)+"\"}"

            return HttpResponse(data)
        elif options == 'groupsinfolist':
            tj=Vre(request.POST.get('tj', ''))
            page = int(request.POST.get('page','1').encode('latin-1', 'ignore').strip())
            num = int(request.POST.get('num','15').encode('latin-1', 'ignore').strip())
            if tj=="":
                groupslist = Group.objects.values().order_by('-id')[(page-1)*num:page*num]
            else:
                groupslist = Group.objects.filter(name__contains=str(tj)).values().order_by('-id')[(page-1)*num:page*num]
            for item in groupslist:
                # groupspermissionlist=[]
                usermembers=[]
                groupspermissionstr = "-"
                # groupspermissionlist =[i for i in Group.objects.get(name=item['name']).permissions.all()]
                for i in Group.objects.get(name=item['name']).permissions.filter():
                    #codename是执行的字符串
                    # groupspermissionlist.append(i.codename)
                    #name是要显示的中文字段
                    groupspermissionstr += i.name.encode("utf8")+','
                    # groupspermissionlist.append(i.name)
                # item['groups_permissions'] = str(groupspermissionlist)
                item['groups_permissions'] = groupspermissionstr
                
                for j in Group.objects.get(name=item['name']).user_set.filter():
                    usermembers.append(j.username)
                item['user'] = str(usermembers)
            # all_permissions = Permission.objects.all().values()
            # all_permissionslist = [i['name'] for i in all_permissions]
            # all_gropulist =[]        
            # grouplist_obj = Group.objects.all()
            # for item in grouplist_obj:all_gropulist.append(item.name)
            
            total = Group.objects.count()
            data="{\"rows\":"+json.dumps(list(groupslist),cls=CJsonEncoder)+",\"total\":\""+str(total)+"\"}"
            return HttpResponse(data)
            

        elif options == 'userdel':
            id = request.POST.get('id','').encode('latin-1', 'ignore').strip().split(',')
            try:
                for i in range(len(id)):
                    User.objects.get(id=id[i]).delete()
            except Exception, e:
                pass
            else:
                return HttpResponse('1')
        elif options == 'groupsdel':
            id = request.POST.get('id','').encode('latin-1', 'ignore').strip().split(',')
            try:
                for i in range(len(id)):
                    Group.objects.get(id=id[i]).delete()
            except Exception, e:
                pass
            else:
                return HttpResponse('1')        
        else:pass

def BulidData(request):
    dbname = request.POST.get('dbname')
    # return HttpResponse(dbname)
    ret = FileHandle.BulidNewExcel('/var/www/html/dtop/download/file/excel/',dbname)
    logHandle.ActionRecord(user_name=request.user.first_name,act_module=dbname,act_type='生成',act_detail='New-'+ret+'.xls')
    return HttpResponse(ret)


def download(request,offset):
    # ret = FileHandle.BulidNewExcel('/var/www/html/dtop/download/file/excel/')
    from django.http import StreamingHttpResponse
    def file_iterator(file_name,chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name ='New-'+offset+'.xls'
    response = StreamingHttpResponse(file_iterator('/var/www/html/dtop/download/file/excel/New-'+offset+'.xls'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    logHandle.ActionRecord(user_name=request.user.first_name,act_type='下载',act_detail=the_file_name)
    return response

# def download(request,offset):
#     return HttpResponse(offset)








