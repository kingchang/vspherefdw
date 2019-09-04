"""
create server vsphere_srv foreign data wrapper multicorn options (wrapper 'multicorn.vspherefdw.main.FDW', host 'vsphere_ip', user 'admin@domain', pwd 'password');
"""
from multicorn import ForeignDataWrapper
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
from pyVmomi import vim, vmodl
import pyVim.connect
import ast
import argparse
import atexit
import getpass
import ssl
from multicorn import vspherefdw


class FDW(ForeignDataWrapper):
    
    valid_tables = {'vmlist'}

    def __init__(self, options, columns):
        super(FDW, self).__init__(options, columns)
        self.host = options.get('host', None)
        self.user = options.get('user', None)
        self.pwd = options.get('pwd', None)
        self.port = options.get('port', '443')
        self.table = options.get('table', 'vmlist')
    
    def connection(self):
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        si = pyVim.connect.SmartConnect(host=self.host, user=self.user, pwd=self.pwd, port=self.port, sslContext=context)
        atexit.register(pyVim.connect.Disconnect, si)
        return si
    
    def get_class(self, table, si):
        if table in self.valid_tables:
            classname = 'vspherefdw.' + table
            target = eval(classname)(si)
            return target
        else:
            log_to_postgres('Error on table name: ' + table, ERROR)

    def execute(self, quals, columns):
        si = self.connection()
        target = self.get_class(self.table, si)
        return target.execute(quals, columns)
        
    @property
    def rowid_column(self):     
        return 'name'
        
    def insert(self, new_values):
        return new_values
     
    def update(self, old_values, new_values):
        si = self.connection()
        target = self.get_class(self.table, si)
        target.update(old_values, new_values)
        return new_values
        
    def delete(self, old_values):
        return 1