#-*- coding:utf-8 -*-
import socket


def mainhandle(a):

    ip_port =('192.168.1.51',9999)
    bb = str.encode(a)
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall(bb)

    server_reply = sk.recv(1024)
    # print bytes.decode(server_reply)
    print server_reply
    sk.close()

if __name__ == "__main__":
    while True:
        aa = raw_input("请输入:").strip()
        if aa == "":continue
        mainhandle(str(aa))
