#!/usr/bin/env python
#coding:utf8
'''
@author: ZhaoShen
'''
from __future__ import division
import GlobalValueClass
import threading
import datetime
import ResultClass
from time import sleep
from TaskMethod import *

class ConductClass(object):
    """
                执行类
    """
    def __init__(self):
        """
        """
        self.result_class = ResultClass.ResultClass()
    
    def getInfoMethod_custom(self,task_dt):
        """
        """
        try:
            script_file_name = task_dt.get('script_name','')
            server_ip = task_dt.get('ftp_ip','')
            user_name = task_dt.get('username','')
            value = CustomClass(script_file_name).main(server_ip,user_name)
            value = float(value)
        except:
            value = -1
        return value
    
    def getInfoMethod_cpuused(self,task_dt):
        """
        """
        try:
            value = CpuusedClass().main()
            value = float(value)
        except:
            value = -999
        return value

    def getInfoMethod_memused(self,task_dt):
        """
        """
        
        try:
            value = MemusedClass().main()
            value = float(value)
        except:
            value = -999
        return value

    def getInfoMethod_cpuload(self,task_dt):
        """
        """
        try:
            value = CpuloadClass().main()
            value = float(value)
        except:
            value = -999
        return value
     
    def getInfoMethod_totalprocess(self,task_dt):
        """
        """
        try:
            value = TotalProcessClass().main()
            value = int(value)
        except:
            value = -999
        return value

    def getInfoMethod_netconn(self,task_dt):
        """
        """
        try:
            state = str(task_dt.get('state',''))
            value = NetconnClass().main(state)
            value = int(value)
        except:
            value = -999
        return value

    def getInfoMethod_process(self,task_dt):
        """
        """
        try:
            process_name = str(task_dt.get('process_name',''))
            value = ProcessClass(process_name).main()
            value = int(value)
        except:
            value = -999
        return value
     
    def getInfoMethod_netrec(self,task_dt):
        """
        """
        try:
            net_name = str(task_dt.get('netname',''))
            value = NetClass().mainNetrec(net_name)
        except:
            value = -999
        return value
     
    def getInfoMethod_netsend(self,task_dt):
        """
        """
        try:
            net_name = str(task_dt.get('netname',''))
            value = NetClass().mainNetsend(net_name)
            value = float(value)
        except:
            value = -999
        return value
     
    def getInfoMethod_diskread(self,task_dt):
        """
        """
        try:
            disk_name = str(task_dt.get('diskname',''))
            value = DiskClass().mainDiskread(disk_name)
            value = float(value)
        except:
            value = -999
        return value
     
    def getInfoMethod_diskwrite(self,task_dt):
        """
        """
        try:
            disk_name = str(task_dt.get('diskname',''))
            value = DiskClass().mainDiskwrite(disk_name)
            value = float(value)
        except:
            value = -999
        return value

    def getInfoMethod_diskused(self,task_dt):
        """
        """
        try:
            disk_name = str(task_dt.get('diskname',''))
            value = DiskUsedClass().main(disk_name)
            value = float(value)
        except:
            value = 9999
        return value

    def errorMethod(self,task_dt):
        return 'error info : %s' % str(task_dt)

    def getFrepTime(self,_dt):
        """
        """
        freq = _dt.get('freq',60)
        timesetp = _dt.get('timesetp',3)
        
        def dealTimesetp(freq,timesetp):
            """
            """
            try:
                timesetp = int(timesetp)
            except:
                timesetp = 3
            try:
                freq = int(freq)
            except:
                freq = 60
            return timesetp
        
        timesetp = dealTimesetp(freq, timesetp)
        
        freq = freq / timesetp
        
        return freq,timesetp
    
    
    def dealResultData(self,value_lt,task_dt):
        """
        """
        value_lt = [v  for v in value_lt if v >= 0.0]
        if len(value_lt) < 0:
            value_lt = [-1]
        self.result_class.main(value_lt,task_dt)
    
    
    def getInfoMethod(self,monitor_id,task_type,task_dt):
        """
        """
        while True:
            if monitor_id not in GlobalValueClass.getMonitorIdList():break
            value_lt = []
            freq,timesetp = self.getFrepTime(task_dt)
            for x in xrange(timesetp):
                starttime = datetime.datetime.now()
                value = getattr(self, 'getInfoMethod_%s' % task_type,self.errorMethod)(task_dt)
                value_lt.append(value)
                endtime = datetime.datetime.now()
                seconds = freq - (endtime - starttime).seconds  - x / 3
                if seconds > 0 :
                    sleep(seconds)
            self.dealResultData(value_lt,task_dt) 
        GlobalValueClass.deleteRunMonitorIdList(monitor_id)



    def dealMethod(self):
        """
        """
        monitor_id_lt = GlobalValueClass.getMonitorIdList()
        for monitor_id  in monitor_id_lt:
            if monitor_id in GlobalValueClass.getRunMonitorIdList() : continue
            task_dt = GlobalValueClass.getMonitorTaskDist().get(monitor_id,0)
            task_type = task_dt.get('task_type','')
            ThreadingClass(task_type,task_dt,monitor_id).start()
            GlobalValueClass.setRunMonitorIdList(monitor_id)
    
    def main(self):
        """
        """
        while True:
            starttime = datetime.datetime.now() 
            self.dealMethod()
            endtime = datetime.datetime.now()
            seconds = 20 - (endtime - starttime).seconds
            if seconds > 0:
                sleep(seconds) 


class ThreadingClass(threading.Thread):
    """
    """
    def __init__(self,task_type,task_dt,monitor_id):
        super(ThreadingClass, self).__init__()
        self.task_type = task_type
        self.task_dt = task_dt
        self.monitor_id = monitor_id


    def run(self):
        """
        """
        try:
            ConductClass().getInfoMethod(self.monitor_id,self.task_type,self.task_dt)
        except:
            sleep(3)
            self.run()

    
if __name__ == '__main__':
    pass
