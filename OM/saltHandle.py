#-*- coding:utf-8 -*-
from OM import models
import socket
import rpyc
import json

class saltrun(object):

    def run(self,data):
        self.ip_port =('192.168.0.222',9999)
        self.bb = str.encode(data)
        self.sk = socket.socket()
        self.sk.connect(self.ip_port)
        self.sk.sendall(bb)

        self.server_reply = sk.recv(1024)
        # print bytes.decode(server_reply)
        # print server_reply
        self.sk.close()
        return self.server_reply

def test(data):

    ip_port =('192.168.0.222',9999)
    bb = str.encode(data)
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall(bb)

    server_reply = sk.recv(1024)
    sk.close()


    return server_reply

    # return 'hello world'
    
#rpyc客户端
#接受服务器返回的json数据
def rpyc_run(userlist,command='ls'):
    conn = rpyc.connect('192.168.1.51',11511)
    conn.root.login('OMuser','KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')
    obj = conn.root.Runcommands(userlist,command)
    return str(obj)


def rpyc_server():
    conn = rpyc.connect('192.168.1.51',11511)
    conn.root.login('OMuser','KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')
    #接收dunp类型的字符串
    obj = conn.root.ServerSync()
    server_dict = json.loads(obj)
    for k in server_dict:
        for kk in server_dict[k]:
            ser_update = models.ServerList.objects.filter(server_ip=server_dict[k][kk]['ipv4'])
            if ser_update:
                ser_update.update(server_id=server_dict[k][kk]['id'],server_name=server_dict[k][kk]['host'],\
                    server_ip=server_dict[k][kk]['ipv4'])
            else:
                models.ServerList.objects.create(server_id=server_dict[k][kk]['id'],server_name=server_dict[k][kk]['host'],\
                    server_ip=server_dict[k][kk]['ipv4'])
    # return str(obj)
    return str(obj)





class MainAction(object):

    def __init__(self):
        conn = self.rpyc.connect('192.168.1.51',11511)
        self.conn.root.login('OMuser','KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')

    def  cmd_run(self,command):
        obj = self.conn.root.Runcommands(command)
        return str(obj)


    def sync_server(self):
        obj = self.conn.root.ServerSync()
        server_dict = json.loads(obj)
        for k in server_dict:
            for kk in server_dict[k]:
                ser_update = models.ServerList.objects.filter(server_ip=server_dict[k][kk]['ipv4'])
                if ser_update:
                    ser_update.update(server_id=server_dict[k][kk]['host'],server_name=server_dict[k][kk]['host'],\
                        server_ip=server_dict[k][kk]['ipv4'])
                else:
                    models.ServerList.objects.create(server_id=server_dict[k][kk]['host'],server_name=server_dict[k][kk]['host'],\
                        server_ip=server_dict[k][kk]['ipv4'])
        # return str(obj)
        return str(obj)



class ItemSelect(object):
    def __init__(self):
        group = self.group
        group_user = self.group_user
        user = self.user

    def groupselecet():
        pass

    def groupuserselect():
        pass

    def userselect():
        pass

