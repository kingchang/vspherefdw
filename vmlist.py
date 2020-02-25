"""
CREATE FOREIGN TABLE vmlist (name text,
                             numcpu int,
                             memorysize int,
                             powerstate text,
                             host text,
                             guestos text,
                             ip inet[])
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

    def compare(ip1,ip2):
        if ip1.startswith("192.168.5") and ip2.startswith("192.168.5"):
            return 1
        elif ip1.startswith("211") or ip1.startswith("202") or ip2.startswith("211") or ip2.startswith("202"):
            return -1
        return 0

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
            row['ip'] = []
            for nic in vs.guest.net:
              if nic.network:  # Only return adapter backed interfaces
                 if nic.ipConfig is not None and nic.ipConfig.ipAddress is not None:
                   ipconf = nic.ipConfig.ipAddress
                   for ip in ipconf:
                     if ":" not in ip.ipAddress:  # Only grab ipv4 addresses
                       if ip.ipAddress.startswith("10.10"):
                         continue
                       if ip.ipAddress != '192.168.122.1':
                         row['ip'].append(ip.ipAddress)
            row['ip'].sort()
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
