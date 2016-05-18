#!/usr/bin/env python
#coding:utf8
'''
@author: ZhaoShen
'''
from xml.dom import minidom as minixml
import json
import urllib2
from time import sleep
import GlobalValueClass

class TaskClass():
    """
    """
    def __init__(self):
        """
        """
        self.servers_id_url = 'http://ucw2agent.chinacloudapp.cn:8090/regedit?dname=%s&rname=%s&sname=%s'
        self.task_url = 'http://ucw2monitorweb6.chinacloudapp.cn:8080/mconfget?servid=%s'
        
        
    def getServersInfo(self):
        """
        """
        dom = minixml.parse('/var/lib/waagent/SharedConfig.xml')
        table = dom.getElementsByTagName( "SharedConfig" )[0] 
        develop = table.getElementsByTagName( "Deployment" )[0] 
        role = table.getElementsByTagName( "Role" )[0] 
        service = develop.getElementsByTagName( "Service" )[0] 
        sname = service.getAttribute('name')
        dname = develop.getAttribute('name')
        rname = role.getAttribute('name')
        return dname,rname,sname
    
    def getPageInfo(self,url):
        """
        """
        req = urllib2.Request(url = url)
        page = urllib2.urlopen(req,timeout=30).read()
        return page
    
    def getServersId(self,dname,rname,sname):
        """
        """
        url= self.servers_id_url % (dname,rname,sname)
        try:
            server_id = self.getPageInfo(url)
        except:
            sleep(5)
            return self.getServersId(dname, rname, sname)
        return server_id
    
    def getTaskInfo(self,server_id):
        """
        """
        url = self.task_url % server_id
        try:
            page = self.getPageInfo(url)
            task_dt = json.loads(page)
        except:
            sleep(5)
            return self.getTaskInfo(server_id)
        return task_dt
        
    def dealOriginalTaskDist(self,original_task_dt):
        """
        """
        monitor_id_lt = []
        for task_type,info in original_task_dt.items():
            if isinstance(info,dict):
                monitor_id = info.get('monitor_id')
                monitor_id_lt.append(monitor_id)
                info.update({'task_type':task_type.lower()})
                GlobalValueClass.setMonitorTaskDist(monitor_id, info)
            elif isinstance(info,list):
                for _info in info:
                    if not isinstance(_info,dict):continue
                    monitor_id = _info.get('monitor_id')
                    monitor_id_lt.append(monitor_id)
                    _info.update({'task_type':task_type.lower()})
                    GlobalValueClass.setMonitorTaskDist(monitor_id, _info)
            else:
                pass
        GlobalValueClass.setMonitorIdList(monitor_id_lt)
                
    
    def main(self):
        """
        """
        dname, rname, sname = self.getServersInfo()
        server_id = self.getServersId(dname, rname, sname)
        while True:
            GlobalValueClass.setServerId(server_id)
            original_task_dt = self.getTaskInfo(server_id)
            self.dealOriginalTaskDist(original_task_dt)
            sleep(60)
        
    
if __name__ == '__main__':
    pass


        
        