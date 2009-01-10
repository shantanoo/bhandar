import pexpect
import os
import socket

class Host:
    def __init__(self, *largs, **dargs):
        if not dargs.has_key('name'):
            raise 'Invalid parameters passed'
        self.sys_host = dargs['name']
        self.timeout = 2
        if dargs.has_key('timeout'):
            self.timeout = dargs['timeout']
        self.ssh = 'ssh'
        self.rsh = 'rsh'
        if dargs.has_key('rsh'):
            self.rsh = dargs['rsh']
        if dargs.has_key('ssh'):
            self.ssh = dargs['ssh']
        self.transport = 'ssh'
        if dargs.has_key('transport'):
            self.transport = dargs['transport']
    def get_hostname(self):
        return self.host
    def set_hostname(self, name):
        if name:
            self.host = name
            return
        ret = self.run('hostname')
        self.host = ''
        if ret == 'ESSH':
            return 'ERR'
        if type(ret) == type(''):
            return ret
        if not ret[1]:
            self.host = ret[0].rstrip()
            return self.host
        return 'ERR'
    def set_platform(self, plat=None):
        if plat:
            self.plat = plat
            return
        ret = self.run_ssh('uname')
        if ret == 'ESSH':
            return 'ERR'
        if not ret[1]:
            self.plat = ret[0].rstrip()
            return self.plat
        return 'ERR'
    def get_platform(self):
        return self.plat
    def ping(self,no=2):
        self.ping = os.system('ping -c '+str(no)+' '+self.sys_host)
        return self.ping
    def isalive(self):
        return self.ping()
    def set_user(self, user):
        self.user = user
    def set_passwd(self, passwd):
        self.passwd = passwd
    def set_hostid(self, hostid=None):
        if hostid:
            self.hostid = hostid
            return
        ret = self.run_ssh('hostid')
        if ret == 'ESSH':
            return 'ERR'
        if not ret[1]:
            self.hostid = ret[0].rstrip()
            return self.hostid
        return 'ERR'
    def get_hostid(self):
        return self.hostid
    def set_ip(self, ip = None):
        if ip:
            self.ip = ip
            return
        try:
            self.ip = socket.gethostbyname(self.sys_host)
        except:
            return 'ERR'
    def get_ip(self):
        try:
            if self.ip:
                return self.ip
        except:
            return None
    def run_rsh(self, cmd):
        try:
            run_cmd = self.rsh + ' -l ' + self.user + ' ' + self.sys_host + ' ' + "'" + cmd + "'"
            s = pexpect.run(run_cmd, events={'(?i)password':self.passwd+"\n"}, withexitstatus=1, timeout=2)
            a = s[0].split('\r\n')
            if a[0].find('not resolve hostname') != -1:
                return 'ERESOLVE'
            if a[0].startswith('Password') or a[0].find("'s password: ") != -1:
                a=a[1:]
            a = '\r\n'.join(a)
            b = s[1]
            del(s)
            return (a,b) 
        except:
            return 'ERSH'
    def run_ssh(self, cmd):
        try:
            run_cmd = self.ssh + ' ' + self.user + '@' + self.sys_host + ' ' + "'" + cmd + "'"
            s = pexpect.run(run_cmd, events={'(?i)password':self.passwd+"\n", 'Are you sure you want to continue connecting':"yes\n"},withexitstatus=1, timeout=self.timeout)
            a = s[0].split('\r\n')

            if a[0].find('not resolve hostname') != -1:
                return 'ERESOLVE'
            if a[0].startswith('Password') or a[0].find("'s password: ") != -1:
                a=a[1:]
            a = '\r\n'.join(a)
            b = s[1]
            del(s)
            return (a,b) 
        except:
            return 'ESSH'
    def run(self, cmd):
        if self.transport == 'rsh':
            return self.run_rsh(cmd)
        elif self.transport == 'ssh':
            return self.run_ssh(cmd)
        else:
            raise self.transport + ' not yet supported'
    def set(self, *largs, **dargs):
        retval = {}
        if dargs.has_key('hostname'):
            retval['hostname'] = self.set_hostname(dargs['hostname'])
        if dargs.has_key('platform'):
            retval['platform'] = self.set_platform(dargs['platform'])
        if dargs.has_key('user'):
            retval['user'] = self.set_user(dargs['user'])
        if dargs.has_key('passwd'):
            retval['passwd'] = self.set_passwd(dargs['passwd'])
        if dargs.has_key('hostid'):
            retval['hostid'] = self.set_hostid(dargs['hostid'])
        if dargs.has_key('ip'):
            retval['ip'] = self.set_ip(dargs['ip'])
        return retval
    def get(self, *largs, **dargs):
        retval = {}
        for key in largs:
            if key == 'hostname':
                retval[key] = self.get_hostname()
            elif key == 'platform':
                retval[key] = self.get_platform()
            elif key == 'hostid':
                retval[key] = self.get_hostid()
            elif key == 'ip':
                retval[key] = self.get_ip()
            else:
                retval[key] = None
        return retval
