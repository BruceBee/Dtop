#-*- coding:utf-8 -*-
import socket
import salt.client

ip_port = ('192.168.0.222',9999)

sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

def run(command):
	local = salt.client.LocalClient()
	ret=local.cmd('*', 'cmd.run', [command])
	print ret
	return ret

while True:
    print '等待客户端连接...'
    conn,addr = sk.accept()
    client_data = conn.recv(1024)
    if client_data == "":continue
    print client_data
    ret = run(client_data)
    print '返回数据'
    # print type(client_data)
    cc = str.encode(str(ret))
    conn.sendall(cc)
    conn.close()

