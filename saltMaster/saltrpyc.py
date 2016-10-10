# -*- coding: utf-8 -*-
import time
import os, sys
import re
from cPickle import dumps
from rpyc import Service
from rpyc.utils.server import ThreadedServer
import ConfigParser
import logging, salt.client
import json

# salt执行cmd

local = salt.client.LocalClient()


def run(userlist, command):
    # local = salt.client.LocalClient()
    # ret=local.cmd('*', 'cmd.run', [command])
    # 此时得到的userlist ='server_id|server_ip;server_id|server_ip;'类似的字符串
    user_str = userlist.split(";")
    user_list = []
    for i in range(len(user_str)):
        user_list.append(user_str[i].split("|")[0])
    ret = local.cmd(user_list, 'cmd.run', [command], expr_form='list')
    return json.dumps(ret)


def SerInfoColl():
    local = salt.client.LocalClient()
    commanInfo = local.cmd('*', 'grains.items')
    diskInfo = local.cmd('*', 'disk.usage')

    ret_dict = {}
    # ret_dict.update({'SerInfo':''})
    for i in commanInfo:
        # print i
        # print commanInfo[i]['localhost']
        # print commanInfo[i]['mem_total']
        # print commanInfo[i]['ipv4']
        # print commanInfo[i]['osfullname']
        ipv4 = str(commanInfo[i]['ipv4']).replace("'127.0.0.1',", "").replace("[", "").replace("]", "").replace("'",
                                                                                                                "").replace(
            " ", "")
        ret_dict[i] = {}
        ret_dict[i].update({'id': commanInfo[i]['id']})
        ret_dict[i].update({'host': commanInfo[i]['localhost']})
        ret_dict[i].update({'mem': commanInfo[i]['mem_total']})
        # ret_dict[i].update({'ipv4':commanInfo[i]['ipv4']})
        ret_dict[i].update({'ipv4': ipv4})
        ret_dict[i].update({'os': commanInfo[i]['osfullname']})

    for i in diskInfo:
        ret_dict[i]['disk'] = {}
        for j in diskInfo[i]:
            # print j,str(int(diskInfo[i][j]['1K-blocks']) / 1024 )+' M'
            ret_dict[i]['disk'].update({j: str(int(diskInfo[i][j]['1K-blocks']) / 1024) + ' M'})
            # print '-----'
    new_dict = {'SerInfo': ret_dict}
    # json
    return json.dumps(new_dict)


# rpyc服务端
# 返回json
class ManagerService(Service):
    def exposed_login(self, user, passwd):
        if user == "OMuser" and passwd == "KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h":
            self.Checkout_pass = True
        else:
            self.Checkout_pass = False

    def exposed_Runcommands(self, userlist, get_string):
        print get_string
        ret = run(str(userlist), str(get_string))
        # print ret
        return ret

    def exposed_ServerSync(self):
        ret = SerInfoColl()
        return ret


s = ThreadedServer(ManagerService, port=11511, auto_register=False)
s.start()
