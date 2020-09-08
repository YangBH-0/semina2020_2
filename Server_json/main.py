#!/usr/bin/env python
# coding: utf-8

# In[1]:


import TcpServer
import json
server = TcpServer.TcpServer()
file_path = './config.json'
with open(file_path, "r") as fj:
    fd = json.load(fj)
    a = fd['PORT']
    b = fd['DB_Host']
    c = fd['DB_User']
    d = fd['DB_name']
    e = fd['DB_password'] 
    f = fd['Specific_table_name']
    g = fd['Device_Register_table_name']
server=TcpServer.TcpServer(a,b,c,d,e,f,g)
server.DB_Con()

while True:
    server.run()


# In[ ]:





# In[ ]:




