# -*- coding: utf-8 -*-
import time
import os,sys
import re
from cPickle import dumps
from rpyc import Service
from rpyc.utils.server import ThreadedServer
import ConfigParser
import logging

def run(command):
    local = salt.client.LocalClient()
    ret=local.cmd('*', 'cmd.run', [command])
    return ret
    
class ManagerService(Service):

    def exposed_login(self,user,passwd):
        if user=="OMuser" and passwd=="KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h":
            self.Checkout_pass=True
        else:
            self.Checkout_pass=False
    
    def exposed_Runcommands(self,get_string):
        print get_string
        ret = run(str(get_string))
        # ret = 'this is a info from server'
        return ret



s=ThreadedServer(ManagerService,port=11511,auto_register=False)
s.start()
