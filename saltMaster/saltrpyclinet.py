import rpyc
conn = rpyc.connect('192.168.1.51',11511)
conn.root.login('OMuser','KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')
obj = conn.root.Runcommands('ls')
print obj
