#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import TcpServer
import json
server = TcpServer.TcpServer()
file_path = './config.json'
with open(file_path, "r") as fj:
    fd = json.load(fj)
    a = fd['PORT']
    b = fd['DB_Host']
    c = fd['DB_User']
    d = fd['DB_password'] 
    e = fd['DB_name']
    f = fd['Specific_table_name']
    g = fd['Device_Register_table_name']
    print(a,b,c,d,e,f,g);
server=TcpServer.TcpServer(a,b,c,d,e,f,g)
server.DB_Con()

while True:
    server.run()

