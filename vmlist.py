"""
CREATE FOREIGN TABLE vmlist (name text, powerstate text, host text) SERVER vsphere_srv OPTIONS ( table 'vmlist');
"""
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
from pyVmomi import vim, vmodl
import time

class vmlist:
    vmList = []

    def __init__(self, si):
        self.si = si
        
    def set_connection(self, si):
        self.si = si
    
    def get_vmList(self):
        si = self.si
        content = si.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)
        vmList = objView.view
        objView.Destroy()
        
        return vmList
        
    def execute(self, quals, columns):
        vmList = self.get_vmList()
        rows = []
        for vm in vmList:
            row = {}
            row['name'] = vm.name
            row['powerstate'] = vm.runtime.powerState
            row['host'] = vm.runtime.host.name
            rows.append(row)
        return rows
        
    @property
    def rowid_column(self):
        return 'name'
        
    def insert(self, new_values):
        return new_values
     
    def update(self, old_values, new_values):
        vmList = self.get_vmList()
        for vm in vmList:
            if (vm.name == old_values):
                if (new_values['powerstate'] == 'poweredOn'):
                    vm.PowerOn()
                elif (new_values['powerstate'] == 'poweredOff'):
                    vm.PowerOff()
        return new_values
                
    def delete(self, old_values):
        return 1