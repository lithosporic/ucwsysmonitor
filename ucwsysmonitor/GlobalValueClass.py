#!/usr/bin/env python
#coding:utf8
'''
@author: ZhaoShen
'''
class GlobalValueClass(): 
    """
    """
    server_id = 0
    monitor_id_lt = []
    run_monitor_id_lt = []
    monitor_task_dt = {}

def setMonitorTaskDist(monitor_id,task_dt):
    """
    """
    GlobalValueClass.monitor_task_dt[monitor_id] = task_dt

def getMonitorTaskDist():
    """
    """
    return GlobalValueClass.monitor_task_dt

def setRunMonitorIdList(monitor_id):
    """
    """
    GlobalValueClass.run_monitor_id_lt.append(monitor_id)

def deleteRunMonitorIdList(monitor_id):
    """
    """
    if monitor_id not in GlobalValueClass.run_monitor_id_lt:return 
    GlobalValueClass.run_monitor_id_lt.remove(monitor_id)

def getRunMonitorIdList():
    """
    """
    return GlobalValueClass.run_monitor_id_lt

def setMonitorIdList(monitor_id_lt):
    """
    """
    GlobalValueClass.monitor_id_lt = monitor_id_lt

def getMonitorIdList():
    """
    """
    return GlobalValueClass.monitor_id_lt

def setServerId(server_id): 
    """
    """
    GlobalValueClass.server_id = server_id
     
def getServerId(): 
    """
    """
    return GlobalValueClass.server_id 
