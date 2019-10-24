"""
CREATE FOREIGN TABLE datastorelist (name text, 
                                    type text, 
                                    multiplehost boolean, 
                                    freespace bigint, 
                                    capacity bigint, 
                                    hostmount text[]) 
                                    SERVER vsphere_srv OPTIONS ( table 'datastorelist');

https://pubs.vmware.com/vi3/sdk/ReferenceGuide/vim.Datastore.html
"""
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
from pyVmomi import vim, vmodl
import time

class datastorelist:
    def __init__(self, si):
        self.si = si
        
    def set_connection(self, si):
        self.si = si
    
    def getList(self):
        si = self.si
        content = si.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.Datastore],
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
            row['type'] = vs.summary.type
            row['multiplehost'] = vs.summary.multipleHostAccess
            row['freespace'] = vs.summary.freeSpace
            row['capacity'] = vs.summary.capacity
            hostList = []
            for host in vs.host:
                hostList.append(host.key.name)
            hostmount = str(hostList).replace('[','{')
            hostmount = hostmount.replace(']','}')
            row['hostmount'] = hostmount
            rows.append(row)
        return rows
        
    @property
    def rowid_column(self):
        return 'name'
        
    def insert(self, new_values):
        return new_values
     
    def update(self, old_values, new_values):
        return new_values
                
    def delete(self, old_values):
        return 1