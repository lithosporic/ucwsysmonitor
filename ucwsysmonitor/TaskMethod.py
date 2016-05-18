#!/usr/bin/env python
#coding:utf8
'''
@author: ZhaoShen
'''
from __future__ import division
import time
from collections import namedtuple
import os
import commands

class CustomClass():
    """
                自定义脚本监控类 
    """
    def __init__(self,script_file_name):
        self.common_path = '/usr/local/ucw/sysmonitor_module/user_script/'
        self.createPathDir(self.common_path)
        self.script_file_name = self.common_path + script_file_name
        self.file_name = script_file_name
    
    def createPathDir(self,path_info):
        path_info = path_info.replace('\\','')
        isExists=os.path.exists(path_info)
        if not isExists:
            os.makedirs(path_info)
    
    def getRemoteFiles(self,server_ip,user_name,task_file_name):
        download_dir = "%s::DATA/%s/ucw_user_script/%s" %(server_ip,user_name,task_file_name)
        command = "rsync --stats -av %s %s" %(download_dir,self.common_path)
        try:
            result = os.system(command)
        except:
            result = os.system(command.encode('utf8'))
        return result
    
    def getFileSuffix(self,script_file_name):
        file_name = str(script_file_name)
        try:
            if file_name.find('.') <> -1:
                suffix_info = file_name.split('.')[-1]
            else:
                suffix_info = 'empty'
        except Exception as e:
            raise 'Get Script File Suffix Exception! Error Info: %s' % e
        return suffix_info
    
   
    def dealPythonScript(self):
        command = 'python %s '% (self.script_file_name)
        command = command.strip()
        num,result = commands.getstatusoutput(command)
        return num,result
        
    def dealShellScript(self):
        command = 'sh %s'% (self.script_file_name)
        command = command.strip()
        num,result = commands.getstatusoutput(command)
        return num,result   


    def dealPerlScript(self):
        command = 'perl %s'% (self.script_file_name)
        command = command.strip()
        num,result = commands.getstatusoutput(command)
        return num,result 
    
    def dealEmpty(self):
        result = -1
        return result 


    def choiceScriptMethod(self,suffix_info):
        _dt = {
               'py':self.dealPythonScript,
               'sh':self.dealShellScript,
               'pl':self.dealPerlScript,
               'empty':self.dealEmpty,
               }
        try:
            method = _dt.get(suffix_info,'empty')
        except Exception as e:
            raise Exception,'Choice Script Method Info Exception ! Error Info : %s'% e
        return method
    
    def dealScriptResultMethod(self,result):
        real_result = 0
        try:
            try:
                _lt = result.split('\n')
            except:
                return result.strip()
            real_result = _lt[-1].strip()
            if len(real_result) == 0: 
                real_result = _lt[-2].strip()
            return real_result
        except:
            return real_result
    
    def main(self,server_ip,user_name):
        if not os.path.isfile(self.script_file_name):
            result = self.getRemoteFiles(server_ip, user_name, self.file_name)
            if result <> 0 : return -1
            
        suffix_info = self.getFileSuffix(self.file_name)
        method = self.choiceScriptMethod(suffix_info)
        num,result = method()
        if num <> 0:
            return -1
        real_result = self.dealScriptResultMethod(result)
        return real_result

class DiskClass(object):
    def __init__(self):
        self.common = '/ucwtest.ucw'
    
    def dealCatalogFormat(self,catalog):
        _dt = {
                '/':'',
              }
        catalog = _dt.get(catalog,catalog)
        return catalog
    
    def cutSpit(self,txt='',head='',tail=''):
        pos=0
        pos=txt.find(head,pos,len(txt))
        if pos < 0:
            return ''
        assert(pos>=0)
        pos+=len(head)    
        oldpos=pos
        pos=txt.find(tail,oldpos,len(txt))
        if pos<0:
            return ''
        return txt[oldpos:pos]
    
    def dealResultInfo(self,result_info):
        _dt  = {
                'b/s':1/1024,
                'kb/s':1,
                'mb/s':1024 ** 1,
                'gb/s':1024 ** 2,
                }
        _info = self.cutSpit(result_info, '10240000', '/s')
        _info = _info.split('s, ')[-1].strip()
        _val,_unit = _info.split(' ')[0],_info.split(' ')[1]
        num = _dt.get(_unit.lower() + '/s',-1)
        result_value = float(_val) * num
        return result_value
        
        
    def deleteTmpTestFile(self,catalog):
        tmp_file = catalog + self.common
        command = 'rm -rf %s' % tmp_file
        result = os.system(command)
        return result
    
    def getDiskOfCatalog(self,disk_name=''):
        if disk_name == '':
            return '/'
        command = 'df'
        result_info = commands.getoutput(command)
        _lt = result_info.split('\n')
        for line in _lt:
            if len(line) == 0: continue
            lt = line.split()
            _name = lt[0].strip()
            catalog = lt[-1].strip()
            if _name.count(disk_name) > 0:
                return catalog
        return '/'
    
    def  getDiskWriteResultInfo(self,catalog=''):
        command = 'dd if=/dev/zero bs=1024 count=10000 of=%s%s' % (catalog,self.common)
        result_info = commands.getoutput(command)
        return result_info

    def  getDiskReadResultInfo(self,catalog=''):
        command = 'dd if=%s%s of=/dev/null bs=1024' % (catalog,self.common)
        result_info = commands.getoutput(command)
        return result_info

    def main(self,disk_name):
        """
        """
        catalog = self.getDiskOfCatalog(disk_name)
        catalog = self.dealCatalogFormat(catalog)
        result_info = self.getDiskWriteResultInfo(catalog)
        write_result =  self.dealResultInfo(result_info)
        result_info =  self.getDiskReadResultInfo(catalog)
        read_result = self.dealResultInfo(result_info)
        self.deleteTmpTestFile(catalog)
        return write_result,read_result
    
    def mainDiskwrite(self,disk_name=''):
        """
        """
        self.common = self.common + 'write'
        write_result = self.main(disk_name)[0]
        return write_result
    
    def mainDiskread(self,disk_name=''):
        """
        """
        self.common = self.common + 'read'
        read_result = self.main(disk_name)[1]
        return read_result


class NetClass(object):
    """
    """
    def __init__(self):
        pass
    
    def getAllInfo(self):
        """
        """
        command = 'cat /proc/net/dev' 
        page = os.popen(command).read()
        return page
    
    def dealAllInfo(self,page):
        """
        """
        page = page.replace('|',' ')
        page = page.replace(':',' ')
        _lt = page.split('\n')
        arg1,arg2 = _lt[0].split()[1],_lt[0].split()[2]
        tag_lt = _lt[1].split()
        tag_lt[tag_lt.index('bytes')] = '%s_bytes' % arg1.lower()
        tag_lt[tag_lt.index('bytes')] = '%s_bytes' % arg2.lower()
        return tag_lt,_lt
    
    def dealZipInfo(self,_lt):
        """
        """
        _dt = {}
        for x,y in _lt:
            if x == 'face':
                _dt[x] = y
            elif x == 'receive_bytes':
                _dt[x] = y
            elif x == 'transmit_bytes':
                _dt[x] = y
        return _dt
                 
            
    def dealInfoList(self,tag_lt,info_lt):
        """
                        处理列表得到数据
                        传入参数：tag_lt 标签列表
                  info_lt 原始数据列表
                        返回值： result_lt 所有网卡的信息
        """
        result_lt = []
        info_lt = [_lt.split() for _lt in info_lt]
        for _lt in info_lt[2:]:
            if len(_lt) == 0: continue
            _dt = self.dealZipInfo(zip(tag_lt,_lt))
            result_lt.append(_dt)
        return result_lt
    
    def main(self,net_name='',_type='receive_bytes'):
        """
        """
        page =  self.getAllInfo()
        tag_lt,_lt = self.dealAllInfo(page)
        result_lt = self.dealInfoList(tag_lt,_lt)
        _bytes = 0
        if net_name == '':
            for _dt in result_lt:
                if _dt.get('face').count('eth') > 0:
                    _bytes += int(_dt.get(_type))
        else:
            for _dt in result_lt:
                if _dt.get('face') == net_name:
                    _bytes = int(_dt.get(_type))
        try:
            _bytes = float(_bytes) / 1024
        except:
            _bytes = -1
        return _bytes
    
    def mainNetrec(self,net_name=''):
        """
        {'receive_bytes': '1025', 'transmit_bytes': '1191', 'face': 'eth0'}
        """
        return self.main(net_name, 'receive_bytes')
    
    def mainNetsend(self,net_name=''):
        """
                        入流量
        {'receive_bytes': '1025', 'transmit_bytes': '1191', 'face': 'eth0'}
        """
        return self.main(net_name, 'transmit_bytes')
        
class ProcessClass(object):
    """
    """
    def __init__(self,process_name=''):
        """
        """
        self.process_name = self.dealProcessNameFormat(process_name)
    
    def dealProcessNameFormat(self,process_name):
        """
        """
        if len(process_name) > 0:
            return process_name
        else:
            return '""'
    
    def dealResultGetNum(self,result):
        """
        """
        num = 0
        for info in result.split('\n'):
            if info.count(str(self.process_name)) > 0 and info.count('grep') ==  0 :
                num += 1
        return num
    
    def getProcessNumber(self):
        """
        """
        command = 'ps -ef |grep %s' % self.process_name
        result =  commands.getoutput(command).strip()
        return self.dealResultGetNum(result)
        
    def main(self):
        """
                    主函数
        """
        return self.getProcessNumber()


class TotalProcessClass(object):
    """
                进程总数类
    """
    def __init__(self):
        pass
    
    def getTotalProcessNumber(self):
        """
                        获得当前运行进程总数信息
        """
        pids = [subdir for subdir in os.listdir('/proc') if subdir.isdigit()]
        return len(pids)
    
    def main(self):
        """
                    主函数
        """
        return self.getTotalProcessNumber()

class CpuloadClass(object):
    """
                系统平均负载类
    """
    def __init__(self):
        pass
    
    def getCpuloadInfo(self):
        """
        """
        loadavg = {} 
        with open("/proc/loadavg",'r') as f:
            con = f.read().split() 
        loadavg['lavg_1']=con[0] 
        loadavg['lavg_5']=con[1] 
        loadavg['lavg_15']=con[2] 
        loadavg['nr']=con[3] 
        loadavg['last_pid']=con[4] 
        
        return loadavg['lavg_15']
    
    def main(self):
        """
        """
        return self.getCpuloadInfo()
    

class NetconnClass(object):
    """
    """
    def __init__(self):
        pass
    def getTcpConnNumber(self,state):
        """
        """
        command = "netstat -an |grep '%s' |grep 'tcp' |wc -l  " % state
        info = os.popen(command).read().strip()
        return info
    
    def main(self,state=''):
        """
        """
        return self.getTcpConnNumber(state)
    
class MemusedClass(object):
    """
                内存类
    """
    def __init__(self):
        pass

    def usagePercent(self,used, total):
        """
        """
        try:
            ret = (used / total) * 100
        except ZeroDivisionError:
            ret = 0
        return round(ret, 1)
    
    def virtualMemory(self):
        """
        """
        PAGE_SIZE = os.sysconf('SC_PAGE_SIZE')
        total = os.sysconf('SC_PHYS_PAGES') * PAGE_SIZE
        free = avail = os.sysconf('SC_AVPHYS_PAGES') * PAGE_SIZE
        used = total - free
        percent = self.usagePercent(used, total)
        svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free'])
        return svmem(total, avail, percent, used, free)
    
    def main(self):
        """
        """
        return self.virtualMemory()[2]

class CpuusedClass(object):
    """
    """
    def __init__(self):
    
        self.scputimes = namedtuple('scputimes', self._get_cputimes_fields())
        self.CLOCK_TICKS = os.sysconf("SC_CLK_TCK")
        self._last_cpu_times = self.cpu_times()
        self._last_per_cpu_times = self.cpu_times(percpu=True)
    
    def _get_cputimes_fields(self):
        with open('/proc/stat', 'rb') as f:
            values = f.readline().split()[1:]
        fields = ['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
        vlen = len(values)
        if vlen >= 8:
            # Linux >= 2.6.11
            fields.append('steal')
        if vlen >= 9:
            # Linux >= 2.6.24
            fields.append('guest')
        if vlen >= 10:
            # Linux >= 3.2.0
            fields.append('guest_nice')
        return fields
    
    def cpu_times2(self):
        with open('/proc/stat', 'rb') as f:
            values = f.readline().split()
        fields = values[1:len(self.scputimes._fields) + 1]
        fields = [float(x) / self.CLOCK_TICKS for x in fields]
        return self.scputimes(*fields)
    
    def per_cpu_times(self):
        cpus = []
        with open('/proc/stat', 'rb') as f:
            # get rid of the first line which refers to system wide CPU stats
            f.readline()
            for line in f:
                if line.startswith(b'cpu'):
                    values = line.split()
                    fields = values[1:len(self.scputimes._fields) + 1]
                    fields = [float(x) / self.CLOCK_TICKS for x in fields]
                    entry = self.scputimes(*fields)
                    cpus.append(entry)
            return cpus
    
    def cpu_times(self,percpu=False):
        """Return system-wide CPU times as a namedtuple.
        """
        if not percpu:
            return self.cpu_times2()
        else:
            return self.per_cpu_times()
    
    def cpu_percent(self,interval=None, percpu=False):
        """
    
        """
        blocking = interval is not None and interval > 0.0
    
        def calculate(t1, t2):
            t1_all = sum(t1)
            t1_busy = t1_all - t1.idle
    
            t2_all = sum(t2)
            t2_busy = t2_all - t2.idle
    
            # this usually indicates a float precision issue
            if t2_busy <= t1_busy:
                return 0.0
    
            busy_delta = t2_busy - t1_busy
            all_delta = t2_all - t1_all
            busy_perc = (busy_delta / all_delta) * 100
            return round(busy_perc, 1)
    
        # system-wide usage
        if not percpu:
            if blocking:
                t1 = self.pu_times()
                time.sleep(interval)
            else:
                t1 = self._last_cpu_times
            _last_cpu_times = self.cpu_times()
            return calculate(t1, _last_cpu_times)
        # per-cpu usage
        else:
            ret = []
            if blocking:
                tot1 = self.cpu_times(percpu=True)
                time.sleep(interval)
            else:
                tot1 = self._last_per_cpu_times
            _last_per_cpu_times = self.cpu_times(percpu=True)
            for t1, t2 in zip(tot1, _last_per_cpu_times):
                ret.append(calculate(t1, t2))
            return ret

    def main(self):
        """
        """
        return float(self.cpu_percent(interval=1,percpu=True)[0])
        
class DiskUsedClass(object):
    """
    """
    def __init__(self):
        pass

    def getAllInfo(self):
        """
        """
        command = 'df' 
        num,page = commands.getstatusoutput(command)
        return num,page
    
    def dealInfo(self,info):
        """
        """
        _lt = info.split()
        _lt.reverse()
        _tmp = [x for x in _lt if x.count('%') > 0]
        result = _tmp[0].replace('%','')
        return result
    
    def getResultValue(self,disk_name):
        """
        """
        num,page = self.getAllInfo()
        if num <> 0 :
            return -1
        _lt = page.split('\n')
        if disk_name == '':
            tmp_lt  = [lt.split()[-1].strip() for lt in _lt]
            x = tmp_lt.index('/')
            
        else:
            tmp_lt  = [lt.split()[0].strip() for lt in _lt]
            tmp = [info for info in tmp_lt if info.count(disk_name)]
            if len(tmp) == 0:
                tmp_lt  = [lt.split()[-1].strip() for lt in _lt]
                tmp = '/'
            else:
                tmp = tmp[0]
            x = tmp_lt.index(tmp)
        
        info = _lt[x]
        disk_percent = self.dealInfo(info)
        return disk_percent
    
    def main(self,disk_name=''):
        """
        """
        return self.getResultValue(disk_name)


if __name__ == '__main__':
    pass
