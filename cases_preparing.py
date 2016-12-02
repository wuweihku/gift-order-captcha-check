# -*- coding: utf8 -*-
import urllib.parse   
import urllib.request         
import csv   
import time  
import hashlib       
import json

'''
CasesPreparing类，用于准备测试用例

'''

class CasesPreparing():   
    appid = '1105260001'
    appkey = 'f46806d675f16feae23b5c07d4a3c935'
    
    info = {
           'action':'', 
           'phone':'',
           'giftID':'',
           'sign':''
            }
 
    def makecases(self,normal_case = True):
        global Totalcounts                                             
        Totalcounts += 1
        data = self.info

        data['action'] = 'getCaptchaCheck'
        data['phone'] = '15888888888'
        data['giftID'] = str(Totalcounts)

        sign_data = self.appid + data['phone'] + self.appkey
        sign = hashlib.md5()
        sign.update(sign_data.encode('utf-8'))
        sign_md5_data = sign.hexdigest()
        data['sign'] = sign_md5_data

        f=open('csv/stresscases.csv','a+') 
        case = data['action'] + ',' + data['phone'] + ',' + data['giftID'] + ',' + data['sign'] + '\n'
        f.write(case)
        f.close()

if __name__ == '__main__':
    
    global Totalcounts
    Totalcounts = 0

    casesnum = 50000
    producer = CasesPreparing()
    global Totalcounts
    Totalcounts = 0

    for i in range(casesnum):
        producer.makecases()
        print('正在生成第 %d 条压测用例' %i)


