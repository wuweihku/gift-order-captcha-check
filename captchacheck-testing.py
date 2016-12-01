import unittest
import urllib.parse    
import urllib.request   
import csv 
import sys  
import hashlib
import json  
import time    

# 对应接口：市场礼包领取验证码前校验接口
# http://activityapi.qa.15166.com/gift-order-captcha-check

class test_captchacheck(unittest.TestCase):
    url = 'http://activityapi.qa.15166.com/gift-order-captcha-check'
    appid = '1105260001'
    appkey = 'f46806d675f16feae23b5c07d4a3c935'

    def setUp(self):  
        pass

    def tearDown(self):
        pass

    def test_captchacheck_cases(self):
        with open('csv/data.csv') as csvfile: 
            reader = csv.DictReader(csvfile)   
            signup_num=0  
            for row in reader: 
                signup_num+=1
                with self.subTest(row=row): 
                    print("正在为'市场礼包领取验证码前校验接口'执行第 %d 条测试数据"%signup_num)

                    info = {
                            'action': row['action'], 
                            'phone':row['phone'],
                            'giftID':row['giftID'],
                            'sign':''
                           }

                    sign_data = test_captchacheck.appid + info['phone'] + test_captchacheck.appkey
                    sign = hashlib.md5() 
                    sign.update(sign_data.encode('utf-8'))
                    sign_md5_data = sign.hexdigest()
                    info['sign'] = sign_md5_data 

                    postdata = urllib.parse.urlencode(info).encode('utf-8') 
                    response = urllib.request.urlopen(self.url, postdata).read()
                    response_dict = json.loads(response.decode())     

                    self.assertEqual(response_dict['code'], eval(row['code']))

        print("----------------------------------------------------------------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()



