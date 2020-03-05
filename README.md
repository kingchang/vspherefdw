# vspherefdw
vspherefdw is a PostgreSQL foreign data wrapper to query your VMware vSphere service.

## Features:
- Table: vmlist
  - List all virtual machines.
  - Power On or Off the specified virtual machine.
- Table: hostlist
  - List all vSphere hosts.
- Table: datastorelist
  - List all datastores

### Sample of "vmlist" table
```
postgres=# SELECT numcpu, memorysize,diskinfo, powerstate, host, ip FROM vmlist;
          name         | numcpu | memorysize | diskinfo |powerstate |     host      |       ip
-----------------------+--------+------------+------------+---------------+-----------------
 VM-121                |     8  |      16384 | [{"label": "Hard disk 1", "disk_capacityInGB": 100.0}] | poweredOn  | 192.168.1.5   | {'192.168.2.217'}
 VM-122                |     8  |      16384 | [{"label": "Hard disk 1", "disk_capacityInGB": 0.1}, {"label": "Hard disk 2", "disk_capacityInGB": 99.88}] | poweredOn  | 192.168.1.6   | {'192.168.2.154'}
 VM-115                |     8  |      16384 | [{"label": "Hard disk 1", "disk_capacityInGB": 100.0}]  | poweredOn  | 192.168.1.3   | {'192.168.2.242'}
 VM-111                |     8  |      16384 | [{"label": "Hard disk 1", "disk_capacityInGB": 100.0}] | poweredOn  | 192.168.1.3   | {'192.168.2.206'}
 VM-102                |     8  |      16384 | [{"label": "Hard disk 1", "disk_capacityInGB": 100.0}] | poweredOn  | 192.168.1.4   | {'192.168.2.37'}
 VM-092                |     8  |      16384 | [{"label": "Hard disk 1", "disk_capacityInGB": 100.0},{"label": "Hard disk 2", "disk_capacityInGB": 200.0}] | poweredOn  | 192.168.1.2   | {'192.168.2.55'}
 VM-052                |     8  |      16384 | [{"label": "Hard disk 1", "disk_capacityInGB": 100.0},{"label": "Hard disk 2", "disk_capacityInGB": 200.0},{"label": "Hard disk 3", "disk_capacityInGB": 1000.0}]  | poweredOff | 192.168.1.1   | {'192.168.2.56'}
```

### Sample of "hostlist" table
```
      name    | cluster    | connstate | maintenance | cpuusage | cpuoverall | memoryusage | memoryoverall
--------------+------------+-----------+-------------+----------+------------+-------------+---------------
 192.168.1.2 | MYCLUSTER  | connected | f           |     6433 |      41961 |      149937 |        262114
 192.168.1.4 | MYCLUSTER  | connected | f           |    18334 |      41961 |      247289 |        393186
 192.168.1.6 | MYCLUSTER  | connected | f           |    18899 |      83923 |      324347 |        392509
 192.168.1.7 |            | connected | f           |     1524 |      41961 |       14288 |         16355 
 192.168.1.3 | MYCLUSTER  | connected | f           |    15827 |      41961 |      245547 |        393186
 192.168.1.1 | MYCLUSTER  | connected | f           |    11883 |      41961 |      175103 |        261827
 192.168.1.5 | MYCLUSTER  | connected | f           |    13112 |      83923 |      335911 |        392509
```

### Sample of "datastorelist" table
```
      name       | type | multiplehost |   freespace   |   capacity    |                                             hostmount
-----------------+------+--------------+---------------+---------------+---------------------------------------------------------------------------------------------------
 datastore_ESXI06 | VMFS | f            |  289962721280 |  290984034304 | {'192.168.1.6'}
 datastore_ESXI07 | VMFS | f            | 2952075935744 | 7186017157120 | {'192.168.1.7'}
 datastore_ESXI04 | VMFS | f            |  289962721280 |  290984034304 | {'192.168.1.4'}
 datastore_ESXI05 | VMFS | f            |  289962721280 |  290984034304 | {'192.168.1.5'}
 datastore_ESXI01 | VMFS | f            |  290231156736 |  291252469760 | {'192.168.1.1'}
 datastore_ESXI02 | VMFS | f            |  289962721280 |  290984034304 | {'192.168.1.2'}
 datastore_ESXI03 | VMFS | f            |  289962721280 |  290984034304 | {'192.168.1.3'}
 DataStore2       | VMFS | t            | 2034656870400 | 4397778075648 | {'192.168.1.6','192.168.1.2','192.168.1.5','192.168.1.4','192.168.1.3','192.168.1.1'}
 DataStore1       | VMFS | t            |  549563924480 |  643976658944 | {'192.168.1.6','192.168.1.2','192.168.1.5','192.168.1.4','192.168.1.3','192.168.1.1'}
 DataStore3       | VMFS | t            | 1893419974656 | 4294698860544 | {'192.168.1.6','192.168.1.2','192.168.1.5','192.168.1.4','192.168.1.3','192.168.1.1'}
 DataStore4       | VMFS | t            | 2316055871488 | 4294698860544 | {'192.168.1.6','192.168.1.2','192.168.1.5','192.168.1.4','192.168.1.3','192.168.1.1'}

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

- In PostgreSQL, the following needs to be excuted first as a superuser.
- Grant permission to normal role vsphere.
```
CREATE EXTENSION multicorn;
GRANT USAGE ON FOREIGN DATA WRAPPER multicorn TO vsphere;
```

- Query as a normal user vsphere.

```
CREATE SERVER vsphere_srv FOREIGN DATA WRAPPER multicorn OPTIONS (wrapper 'multicorn.vspherefdw.main.FDW', host 'vsphere_ip', user 'admin@domain', pwd 'password');
```
## Create foreign table you need
### Table: vmlist
- Do not modify the column name.
- Memroy unit: MB
```
CREATE FOREIGN TABLE vmlist (name text,
                             numcpu int,
                             memorysize int,
                             diskInfo jsonb,
                             powerstate text,
                             host text,
                             guestos text,
                             ip inet)
                             SERVER vsphere_srv OPTIONS ( table 'vmlist');
```
- Query your virtual machine
```
SELECT * FROM vmlist; -- List all virtual machines
UPDATE vmlist SET powerstate = 'poweredOn' WHERE name = 'VM5432'; -- Power On machine "VM5432"
UPDATE vmlist SET powerstate = 'poweredOff' WHERE name = 'VM5432'; -- Power Off machine "VM5432"
```

### Table: hostlist
- Do not modify the column name.
- CPU unit: MHz
- Memory unit: MB
```
CREATE FOREIGN TABLE hostlist (name text, 
                               cluster text, 
                               connstate text, 
                               maintenance boolean, 
                               cpuusage int, 
                               cpuoverall int, 
                               memoryusage int, 
                               memoryoverall int) 
                               SERVER vsphere_srv OPTIONS ( table 'hostlist');
```
- Query your vSphere hosts
```
SELECT * FROM hostlist; -- List all vSphere hosts
```

### Table: datastorelist
- Do not modify the column name.
- Unit: Bytes
```
CREATE FOREIGN TABLE datastorelist (name text, 
                                    type text, 
                                    multiplehost boolean, 
                                    freespace bigint, 
                                    capacity bigint, 
                                    hostmount text[]) 
                                    SERVER vsphere_srv OPTIONS ( table 'datastorelist');
```
- Query your datastores
```
SELECT * FROM datastorelist; -- List all datastores
```
