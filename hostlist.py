"""
CREATE FOREIGN TABLE hostlist (name text, 
                               cluster text, 
                               connstate text, 
                               maintenance boolean, 
                               cpuusage int, 
                               cpuoverall int, 
                               memoryusage int, 
                               memoryoverall int) 
                               SERVER vsphere_srv OPTIONS ( table 'hostlist');

https://pubs.vmware.com/vi3/sdk/ReferenceGuide/vim.HostSystem.html
"""
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
from pyVmomi import vim, vmodl
import time

class hostlist:
    def __init__(self, si):
        self.si = si
        
    def set_connection(self, si):
        self.si = si
    
    def getList(self):
        si = self.si
        content = si.content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.HostSystem],
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
            if isinstance(vs.parent, vim.ClusterComputeResource):
                row['cluster'] = vs.parent.name
            else:
                row['cluster'] = ''
            row['connstate'] = vs.runtime.connectionState
            row['maintenance'] = vs.runtime.inMaintenanceMode
            row['cpuusage'] = vs.summary.quickStats.overallCpuUsage
            row['cpuoverall'] = int(vs.hardware.cpuInfo.hz * vs.hardware.cpuInfo.numCpuCores / 1024 / 1024)
            row['memoryusage'] = vs.summary.quickStats.overallMemoryUsage
            row['memoryoverall'] = int(vs.hardware.memorySize / 1024 / 1024)
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