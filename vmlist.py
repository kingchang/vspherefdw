"""
CREATE FOREIGN TABLE vmlist (name text, 
                             numcpu int, 
                             memorysize int, 
                             powerstate text, 
                             host text, 
                             guestos text, 
                             ip inet) 
                             SERVER vsphere_srv OPTIONS ( table 'vmlist');
                             
https://pubs.vmware.com/vi3/sdk/ReferenceGuide/vim.VirtualMachine.html                             
"""
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
from pyVmomi import vim, vmodl
import time

class vmlist:
    def __init__(self, si):
        self.si = si
        
    def set_connection(self, si):
        self.si = si
    
    def getList(self):
        si = self.si
        content = si.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)
        vsList = objView.view
        objView.Destroy()
        
        return vsList
        
    def execute(self, quals, columns):
        vsList = self.getList()
        rows = []
        for vs in vsList:
            row = {}
            row['name'] = vs.name
            row['numcpu'] = vs.summary.config.numCpu
            row['memorysize'] = vs.summary.config.memorySizeMB
            row['powerstate'] = vs.runtime.powerState
            row['host'] = vs.runtime.host.name
            row['guestos'] = vs.summary.guest.guestFullName
            row['ip'] = vs.summary.guest.ipAddress
            rows.append(row)
        return rows
        
    @property
    def rowid_column(self):
        return 'name'
        
    def insert(self, new_values):
        return new_values
     
    def update(self, old_values, new_values):
        vmList = self.getList()
        for vm in vmList:
            if (vm.name == old_values):
                if (new_values['powerstate'] == 'poweredOn'):
                    vm.PowerOn()
                elif (new_values['powerstate'] == 'poweredOff'):
                    vm.PowerOff()
        return new_values
                
    def delete(self, old_values):
        return 1