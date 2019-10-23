# vspherefdw
vspherefdw is a PostgreSQL foreign data wrapper to query your VMware vSphere service.

## Features:
- Table: vmlist
  - List all virtual machines.
  - Power On or Off the specified virtual machine.
- Table: hostlist
  - List all vSphere hosts.

### Sample of "vmlist" table
```
postgres=# SELECT numcpu, memorysize, powerstate, host, ip FROM vmlist;
          name         | numcpu | memorysize | powerstate |     host      |       ip
-----------------------+--------+------------+------------+---------------+-----------------
 VM-121                |     8  |      16384 | poweredOn  | 192.168.1.5   | 192.168.2.217
 VM-122                |     8  |      16384 | poweredOn  | 192.168.1.6   | 192.168.2.154
 VM-115                |     8  |      16384 | poweredOn  | 192.168.1.3   | 192.168.2.242
 VM-111                |     8  |      16384 | poweredOn  | 192.168.1.3   | 192.168.2.206
 VM-102                |     8  |      16384 | poweredOn  | 192.168.1.4   | 192.168.2.37
 VM-092                |     8  |      16384 | poweredOn  | 192.168.1.2   | 192.168.2.55
 VM-052                |     8  |      16384 | poweredOff | 192.168.1.1   | 192.168.2.56
```

### Sample of "hostlist" table
```
     name    | cluster    | connstate | maintenance | cpuusage | cpuoverall | memoryusage | memoryoverall
-------------+------------+-----------+-------------+----------+------------+-------------+---------------
 192.168.1.2 | MYCLUSTER  | connected | f           |     6433 |      41961 |      149937 |        262114
 192.168.1.4 | MYCLUSTER  | connected | f           |    18334 |      41961 |      247289 |        393186
 192.168.1.6 | MYCLUSTER  | connected | f           |    18899 |      83923 |      324347 |        392509
 192.168.1.7 |            | connected | f           |     1524 |      41961 |       14288 |         16355 
 192.168.1.3 | MYCLUSTER  | connected | f           |    15827 |      41961 |      245547 |        393186
 192.168.1.1 | MYCLUSTER  | connected | f           |    11883 |      41961 |      175103 |        261827
 192.168.1.5 | MYCLUSTER  | connected | f           |    13112 |      83923 |      335911 |        392509
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
```
CREATE FOREIGN TABLE vmlist (name text, numcpu int, 
                             memorysize int, 
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
