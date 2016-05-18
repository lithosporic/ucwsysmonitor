#!/usr/bin/env python
#coding:utf8
'''
@author: ZhaoShen
'''
import threading
import TaskClass
import ConductClass
from time import sleep
__VERSIONS__ = '1.01'

class ConfigClass():
    PROGRAM_TYPE = [
                    'task',
                    'conduct',
                    ]
    PROGRAM_CLASS_DIST = {
                    'task':TaskClass.TaskClass(),
                    'conduct':ConductClass.ConductClass(),
                    }

class ThreadingClass(threading.Thread):
    def __init__(self,config_class,_type):
        super(ThreadingClass, self).__init__()
        self._class = config_class
        self._type = _type

    def run(self):
        try:
            self._class = config_class.PROGRAM_CLASS_DIST.get(self._type)
            self._class.main()
        except :
            sleep(5)
        finally:
            self.run()

  
if __name__ == '__main__':
    print 'system monitor starting ~~'
    config_class = ConfigClass()
    for _type in config_class.PROGRAM_TYPE:
        ThreadingClass(config_class,_type).start()
