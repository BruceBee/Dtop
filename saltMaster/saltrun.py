#-*- coding:utf-8 -*-
import socket
import salt.client

def run():
	local = salt.client.LocalClient()
	ret=local.cmd('*', 'cmd.run', ['whoami'])
	print ret


if __name__ == '__main__':
	run()
