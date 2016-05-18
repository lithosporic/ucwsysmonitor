#!/usr/bin/env python
#coding:utf8
'''
@author: ZhaoShen
'''
import urllib2
import urllib
import json
from time import sleep,time
import GlobalValueClass

class ResultClass(object):
    """
                结果类
    """
    def __init__(self):
        pass
    
    def insertResultData(self,data):
        """
        """
        data = json.dumps(data)
        url = 'http://ucw2monitorweb6.chinacloudapp.cn:8080/sysresult'
        data = {'data':data}
        arg_dt = urllib.urlencode(data)
        req = urllib2.Request(url = url,data = arg_dt)
        try:
            for i in xrange(3):  
                resutl = urllib2.urlopen(req).read()
                if resutl == '1':
                    return 1
                sleep(i/5)
            return 0
        except:
            sleep(1)
            self.insertResultData(data)
    
    def getValue(self,method,value_lt):
        """
        """
        val = 0
        if method.lower() == 'average':
            val = sum(value_lt)/len(value_lt)
        elif method.lower() == 'maximum':
            val = max(value_lt)
        elif method.lower() == 'minimum':
            val = min(value_lt)
        return val
    
    def judgeFlag(self,val,threshold,compare):
        """
        """
        threshold = float(threshold)
        _dt = {
               '>':val > threshold,
               '<':val < threshold,
               '=':val == threshold,
               '>=':val >= threshold,
               '<=':val <= threshold,
               '!=':val <> threshold,
               }
        return _dt.get(compare)
    
    
    def getBaseInfo(self,task_dt):
        """
        """
        yunid = GlobalValueClass.getServerId()
        item_id = task_dt.get('item_id')
        monitor_id = task_dt.get('monitor_id')
        method = task_dt.get('method','average')
        compare = task_dt.get('compare','=')
        threshold = task_dt.get('threshold',0)
        user_id = task_dt.get('user_id','0')
        monitor_type = task_dt.get('task_type','')
        return yunid,item_id,monitor_id,method,compare,threshold,user_id,monitor_type
    
    def getResultData(self,yunid,item_id,monitor_id,value,flag,user_id,monitor_type):
        """
        """
        unixtime = int(time())
        data = {
                 u'monitor_id': monitor_id,
                 u'unixtime': unixtime, 
                 u'value': value, 
                 u'flag': flag, 
                 u'item_id': item_id, 
                 u'yunid': yunid,
                 u'user_id':user_id,
                 u'monitor_type':monitor_type,
                }
        return data
    
    def main(self,value_lt,task_dt):
        """
        """
        yunid,item_id,monitor_id,method,compare,threshold,user_id,monitor_type = self.getBaseInfo(task_dt)
        value = self.getValue(method, value_lt)
        flag = self.judgeFlag(value, threshold, compare)
        data = self.getResultData(yunid,item_id,monitor_id,value,flag,user_id,monitor_type)
        self.insertResultData(data)

if __name__ == '__main__':
    pass
                