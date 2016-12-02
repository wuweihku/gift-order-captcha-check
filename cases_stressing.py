# -*- coding: utf-8 -*-
import urllib.parse  
import urllib.request
import csv 
import time 
import threading 
import queue 

'''
TestAPI类:
__init__()构造函数
stressing()压测函数

'''

class TestAPI():  
    def __init__(self, threadName, url, data):
        self.threadName = threadName  
        self.url = url
        self.data = data 

    def stressing(self):
        global Totalcases

        info = {
               'action':self.data['action'], 
               'phone':self.data['phone'],
               'giftID':self.data['giftID'],
               'sign':self.data['sign']
               }
        Totalcases += 1 
        postdata = urllib.parse.urlencode(info).encode('utf-8')
        response = urllib.request.urlopen(self.url, postdata).read()  
        response_dict = eval(response)

        print('%s Processing: '%self.threadName,'code->%s'%response_dict['code'],'msg->%s'%response_dict['msg'],'\n')


class myThread(threading.Thread):    
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID 
        self.name = 'Thread-%s'%name
        self.q = q  

    def run(self):
        print('Starting ' + self.name)
        process_data(self.name, self.q)
        print('Exiting ' + self.name)

if __name__ == '__main__': 
    url = 'http://activityapi.qa.15166.com/gift-order-captcha-check'

    totalthreads = 1000      #起多少个线程，思想就是一开始就起好所有需要的线程
    casesnum = 1000         #思想就是一开始就将所有需要的cases准备进队列
    duration = 1

    global Totalcases
    global Successed
    global Failed
    Totalcases = 0
    Successed = 0
    Failed = 0
    timestart  = time.time()

    exitFlag = 0
    caseFlag = list(range(1,casesnum+1))
    concurrents = int(totalthreads/10) #单轮并发量，可以用casesnum/concurrents，算出一共需要跑多少round

    def process_data(threadName, q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                print('current case: %s'%(casesnum-workQueue.qsize()+1)) 

                if workQueue.qsize() in caseFlag[::concurrents]: 
                     print('current runround finished, %s seconds waiting for next new runround now.' %duration)
                     time.sleep(duration)

                qdata = q.get()
                queueLock.release()

                threadtestapi = TestAPI(threadName, url, qdata)  
                threadtestapi.stressing() 
            else:
                queueLock.release()
            time.sleep(0.05)

    threadList = list(range(1, totalthreads+1))
    queueLock = threading.Lock()
    workQueue = queue.Queue(casesnum)  
    threads = []
    threadID = 1

    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start() 
        threads.append(thread) 
        threadID += 1

    queueLock.acquire()
    while not workQueue.full():
        with open('csv/stresscases.csv') as csvfile:
            reader = csv.DictReader(csvfile,skipinitialspace=True) 
            totalnum = 0 
            for row in reader:
                totalnum += 1 
                workQueue.put(row)
                if workQueue.full(): 
                    break
    print("%d Testcases Ready "%workQueue.qsize())
    queueLock.release()

    while not workQueue.empty():
        pass

    exitFlag = 1

    for t in threads:
        t.join() 
    print('Exiting Main Thread')

    timefinish = time.time()
    timecost = timefinish-timestart
    print("--------------------\nTotalcases: %d \n"%Totalcases, "Successed: %d \n"%Successed, "   Failed: %d \n"%Failed)
    print('%s seconds cost for testing'%timecost)
