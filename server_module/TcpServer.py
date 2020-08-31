#!/usr/bin/env python
# coding: utf-8

# In[1]:


# PYthon version 3.* 에서만 지원함
# 외부 모듈 socket,pymysql  설치해야함 
# 예외처리가 매우 미흡함으로 나중에 개선할 것 !!!!! 중요 !!!!!
import TcpNet
try:
    import pymysql
except ImportError:
    print('not pymysql')
class TcpServer:
    def __init__(self):
        self.Tcp = TcpNet.TcpNet()
        self.HOST= TcpNet.ipcheck(); # 서버 ip주소 자신의 아이피로 자동 할당
        print("set HOST:"+self.HOST)
        self.PORT=11000 # 포트 는 10000이상으로 쓰고 겹치지 않는지 확인하며 할당 할 것
        self.DB_Host= '203.234.62.115' # DB 주소
        self.DB_User='root' # 접속할 아이디 
        self.DB_password ='1234' # 접속할 아이디의 비밀번호
        self.DB_name = 'MetadataRegistry' # 접속할 DB의 이름
        self.Specific_table_name = 'specific_metadata' # specific_metadata테이블 이름
        self.charset = 'utf8' # 형식
        self.table_name = '' #  데이터넣을 테이블 이름 변수 선언
        self.item_id = ''
        self.Device_Register_table_name = 'device_register' # 디바이스 리스트들은 테이블 이름
        self.conn = pymysql.connect(host=self.DB_Host,user=self.DB_User, password=self.DB_password,db=self.DB_name, charset=self.charset) # DB연결 나중에 예외처리 해줄것
        self.curs = self.conn.cursor() # DB 커서
        print('DB connected.....')
        
    def package_V(self,s): # 문자열 쌓아주는 함수
        return '\''+str(s)+'\''
    def set_Server_HOST(self,h):
        self.HOST=h
    def set_Server_PORT(self,p):
        self.PORT=p
    def set_DB_HOST(self,dh):
        self.DB_Host=dh
    def set_DB_User(self,du):
        self.DB_User=du
    def set_DB_Password(self,dp):
        self.DB_password=dp
    def set_DB_Name(self,dn):
        self.DB_name=dn
    def get_Host(self):
        return self.HOST
    def get_PORT(self):
        return self.PORT
    def get_DB_Name(self):
        return self.DB_name
    def get_DB_HOST(self):
        return self.DB_Host
    def get_DB_User(self):
        return self.DB_User
    def run(self):
        print('waiting')
        self.Tcp.Accept(IP=self.HOST,Port=self.PORT)
        try:
            receive_id=self.Tcp.ReceiveStr()
            print(receive_id)
            self.curs.execute("SELECT system_id,table_name, item_id FROM "+self.DB_name+"."+self.Device_Register_table_name +" WHERE system_id = " +self.package_V(receive_id)+";")
            result = self.curs.fetchone()
            if(result[0] is not None):
                self.table_name=result[1]
                self.item_id=result[2]
                self.Tcp.SendStr('yes')
            else:
                self.Tcp.SendStr('no')
                print('조회가 되질 않습니다')
        except Exception as e :
            self.Tcp.SendStr('no')
            print('error :', e)
        print('Connected............')
        while True:
            ack = self.Tcp.ReceiveStr()
            if(ack=='send'):
                self.Tcp.SendStr('con')
            receive_data=self.Tcp.ReceiveStr()
            print("receive_data:"+receive_data)
            input_data=receive_data.split('!')
            num=self.curs.execute("SELECT metadata_value FROM "+self.DB_name+'.'+self.Specific_table_name+" WHERE item_id = "+self.package_V(self.item_id)+" AND (metadata_key like "+self.package_V('sensor-%')+");") # 특정 table의 칼럼값을 가져옴
            DB_column=self.curs.fetchall()
            DB_sql='INSERT INTO '+ self.table_name+' ( timestamp,'
            for i in DB_column:
                for j in i:
                    DB_sql = DB_sql+j+','
            DB_sql= DB_sql[:len(DB_sql)-1]+') VALUES ('
            a= self.package_V(input_data[0])
            input_data=input_data[1:]
            data_list=[]
            for i in input_data:
                data_list.append(i.split(':'))
            data_dict = dict(data_list)
            input_data=[]
            for i in DB_column:
                for j in i:
                    if j in data_dict:
                        input_data.append(data_dict[j])
                    else:
                        input_data.append('NULL')
            input_data.insert(0,(a))
            s=",".join(input_data)
            DB_sql= DB_sql+s+');'
            self.curs.execute(DB_sql)
            self.conn.commit()
            ack=None
            if receive_data =='exit':
                print('socket end')
                break


# In[ ]:





# In[ ]:




