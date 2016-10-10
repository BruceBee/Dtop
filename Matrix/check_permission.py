#_*_coding:utf-8_*_
from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,render_to_response
from django.template import RequestContext

# perm_dic = {
#     'view_customer_list': ['customer_list','GET',[]],
#     'view_customer_info': ['customer_detail','GET',[]],
#     'edit_own_customer_info': ['customer_detail','POST',['test']],
# }

#总的权限字典

permissions_dic = {
    'info':{
        'add':['/base_data/pagelist/xxxxinfo/add/','POST',[]],
        'mod':['/base_data/pagelist/xxxxxinfo/mod/','POST',[]],
        'del':['/base_data/pagelist/xxxxxinfo/del/','POST',[]],
    },
    'domain':{
        'add':['/dns_data/pagelist/xxxxinfo/add/','POST',[]],
        'mod':['/dns_data/pagelist/xxxxxinfo/mod/','POST',[]],
        'del':['/dns_data/pagelist/xxxxxinfo/del/','POST',[]],
    },
    'set':{
        'exec':['/auto/xxxx/exec/','POST',[]],
    },
    'alarm':{
        'exec':['/alarm/xxxx/exec/','POST',[]],
    },
    'auth':{
        'add':['/auth/pagelist/xxxxinfo/add/','POST',[]],
        'mod':['/auth/pagelist/xxxxinfo/mod/','POST',[]],
        'del':['/auth/pagelist/xxxxinfo/del/','POST',[]],
    }
}




perm_dic = {
    'add_test': ['/authmanagement/add_test/','POST',[]],
    'change_test': ['/authmanagement/change_test/','POST',[]],
    'del_test': ['/authmanagement/del_test/','POST',[]],
    
    #告警信息日志查看、图表展示、告警弹窗权限、删除日志
    'alarminfo_pagedataList':['/alarm_data/alarminfo_pagedataList/','POST',[]],
    'alarminfo_charts':['/alarm_data/alarminfo_charts/','POST',[]],
    'alarminfo_getalert':['/alarm_data/alarminfo_getalert/','POST',[]],
    'alarminfo_deleteFun':['/alarm_data/alarminfo_deleteFun/','POST',[]],

    #云资源信息展示查询、新增修改、删除权限
    'baseinfo_pagedataList':['/base_data/baseinfo_pagedataList/','POST',[]],
    'baseinfo_editFun':['/base_data/baseinfo_editFun/','POST',[]],
    'baseinfo_deleteFun':['/base_data/baseinfo_deleteFun/','POST',[]],

    #配置信息展示查询、新增修改、删除权限
    'configinfo_pagedataList':['/base_data/configinfo_pagedataList/','POST',[]],
    'configinfo_editFun':['/base_data/configinfo_editFun/','POST',[]],
    'configinfo_deleteFun':['/base_data/configinfo_deleteFun/','POST',[]],

    #平台信息展示查询、新增修改、删除权限
    'platforminfo_pagedataList':['/base_data/platforminfo_pagedataList/','POST',[]],
    'platforminfo_editFun':['/base_data/platforminfo_editFun/','POST',[]],
    'platforminfo_deleteFun':['/base_data/platforminfo_deleteFun/','POST',[]],

    #业务线信息展示查询、新增修改、删除权限
    'businessinfo_pagedataList':['/base_data/businessinfo_pagedataList/','POST',[]],
    'businessinfo_editFun':['/base_data/businessinfo_editFun/','POST',[]],
    'businessinfo_deleteFun':['/base_data/businessinfo_deleteFun/','POST',[]],

    #dns信息展示查询、新增修改、删除权限
    'dnsinfo_pagedataList':['/dns_data/dnsinfo_pagedataList/','POST',[]],
    'dnsinfo_editFun':['/dns_data/dnsinfo_editFun/','POST',[]],
    'dnsinfo_deleteFun':['/dns_data/dnsinfo_deleteFun/','POST',[]],

    #域名信息展示查询、新增修改、删除权限
    'domaininfo_pagedataList':['/dns_data/domaininfo_pagedataList/','POST',[]],
    'domaininfo_editFun':['/dns_data/domaininfo_editFun/','POST',[]],
    'domaininfo_deleteFun':['/base_data/domaininfo_deleteFun/','POST',[]],

    #硬件资产信息展示查询、新增修改、删除权限
    'assetinfo_pagedataList':['/asset_data/assetinfo_pagedataList/','POST',[]],
    'assetinfo_editFun':['/asset_data/assetinfo_editFun/','POST',[]],
    'assetinfo_deleteFun':['/asset_data/assetinfo_deleteFun/','POST',[]],

    #版本发布权限
    'autorelease_putdata':['/auto_data/autorelease_putdata/','POST',[]],

    #dns同步
    'recordlist_sync':['/auto_data/recordlist_sync','POST',[]],
    'domainlist_sync':['/auto_data/domainlist_sync','POST',[]],

    #权限系统用户与属组展示查询、新增、修改、删除权限
    'auth_get_grolist_and_perm':['/auth_data/get_groupslist_and_permission/','POST',[]],

    'auth_usrlst':['/auth_data/userinfolist/','POST',[]],
    'auth_usradd':['/auth_data/useradd/','POST',[]],
    'auth_usrmod':['/auth_data/usermod/','POST',[]],
    'auth_usrdel':['/auth_data/userdel/','POST',[]],

    'auth_grplst':['/auth_data/groupsinfolist/','POST',[]],
    'auth_grpadd':['/auth_data/groupsadd/','POST',[]],
    'auth_grpmod':['/auth_data/groupsmod/','POST',[]],
    'auth_grpdel':['/auth_data/groupsdel/','POST',[]],
}

#'字符串'：[url,get/post,参数]
def perm_check(*args,**kwargs):
    request = args[0]
    # url_resovle_obj = resolve(request.path_info)
    # current_url_namespace = url_resovle_obj.url_name
    
    # return False
    url_resovle_obj1 = request.get_full_path().split('/')[1]
    url_resovle_obj2 = request.get_full_path().split('/')[2]
    current_url_namespace = '/'+url_resovle_obj1+'/'+url_resovle_obj2+'/'

    # return current_url_namespace
    #app_name = url_resovle_obj.app_name #use this name later
    print("url namespace:",current_url_namespace)
    matched_flag = False # find matched perm item
    matched_perm_key = None
    if current_url_namespace is not None:#if didn't set the url namespace, permission doesn't work
        print("find perm...")
        for perm_key in perm_dic:
            perm_val = perm_dic[perm_key]
            if len(perm_val) == 3:#otherwise invalid perm data format
                url_namespace,request_method,request_args = perm_val
                print(url_namespace,current_url_namespace)
                if url_namespace == current_url_namespace: #matched the url
                    if request.method == request_method:#matched request method
                        if not request_args:#if empty , pass
                            matched_flag = True
                            matched_perm_key = perm_key
                            print('mtched...')
                            break #no need looking for  other perms
                        else:
                            for request_arg in request_args: #might has many args
                                request_method_func = getattr(request,request_method) #get or post mostly
                                #print("----->>>",request_method_func.get(request_arg))
                                if request_method_func.get(request_arg) is not None:
                                    matched_flag = True # the arg in set in perm item must be provided in request data
                                else:
                                    matched_flag = False
                                    print("request arg [%s] not matched" % request_arg)
                                    break #no need go further
                            if matched_flag == True: # means passed permission check ,no need check others
                                print("--passed permission check--")
                                matched_perm_key = perm_key
                                break

    else:#permission doesn't work
        # 设置True代表不匹配规则时默认放行，False则代表不放行
        return True

    if matched_flag == True:
        #pass permission check
        perm_str = "Matrix.%s" %(matched_perm_key)
        if request.user.has_perm(perm_str):
            print("\033[42;1m--------passed permission check----\033[0m")
            return True
        else:
            print("\033[41;1m ----- no permission ----\033[0m")
            print(request.user,perm_str)
            return False
    else:
        print("\033[41;1m ----- no matched permission  ----\033[0m")
def check_permission(func):

    def wrapper(*args,**kwargs):
        print("---start check perms",args[0])
        if not perm_check(*args,**kwargs):
            return render(args[0],'403.html')
        # aa = perm_check(*args,**kwargs)
        # if aa == '/authmanagement/view_task':
        #     return render(args[0],'403.html')
        return func(*args,**kwargs)
        #print("---done check perms")
    return wrapper

# 50行实现细粒度的权限控制