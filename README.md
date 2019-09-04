# vspherefdw
vspherefdw is a PostgreSQL foreign data wrapper to manage VMware vSphere service.

## Features:
- List all virtual machines.
- Power On or Off the specified virtual machine.

### Sample of "vmlist" table
```
postgres=# select * from vmlist;

                     name                   | powerstate |     host
--------------------------------------------+------------+---------------
 VM-121                                     | poweredOn  | 192.168.1.5
 VM-122                                     | poweredOn  | 192.168.1.6
 VM-115                                     | poweredOn  | 192.168.1.3
 VM-111                                     | poweredOn  | 192.168.1.3
 VM-102                                     | poweredOn  | 192.168.1.4
 VM-092                                     | poweredOn  | 192.168.1.2
 VM-052                                     | poweredOff | 192.168.1.1
```
## Tested Platform
- PostgreSQL 11
- Python 3.6
- Multicorn 1.3.4

## Installation
- Install pyVmomi
```
$ sudo pip install pyVmomi
```

- Find multicorn python path. In my environment: /usr/lib/python3/dist-packages/multicorn
```
$ cd /usr/lib/python3/dist-packages/multicorn
$ sudo git clone https://github.com/ycku/vspherefdw.git
```

- In PostgreSQL, one time in the beginning.
```
CREATE EXTENSION multicorn;
CREATE SERVER vsphere_srv FOREIGN DATA WRAPPER multicorn OPTIONS (wrapper 'multicorn.vspherefdw.main.FDW', host 'vsphere_ip', user 'admin@domain', pwd 'password');
```

- Create foreign table "vmlist".
- Do not modify the schema.
```
CREATE FOREIGN TABLE vmlist (name text, powerstate text, host text) SERVER vsphere_srv OPTIONS ( table 'vmlist');
```
- Query your virtual machine
```
SELECT * FROM vmlist; -- List all virtual machines
UPDATE vmlist SET powerstate = 'poweredOn' WHERE name = 'VM5432'; -- Power On machine "VM5432"
UPDATE vmlist SET powerstate = 'poweredOff' WHERE name = 'VM5432'; -- Power Off machine "VM5432"
```
