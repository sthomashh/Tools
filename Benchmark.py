#!/usr/bin/python
#
# @author:    Sven Thomas, sthomas@gwdg.de

import re
import os
import sys
import time


class Benchmark (object): 
    debug = False
    image_id = ""
    vm_name = ""
    vm_amount = 0
    flavor = 0
    wait_time = 0
    ids_started_vms = ""
    
    def __init__(self, vm_amount=5, flavor=1, vm_name='TEST', wait_time=5.0): 
        self.vm_amount = vm_amount 
        self.flavor = flavor 
        self.vm_name = vm_name
        self.wait_time = wait_time
        
    def setImageId(self, image_id):
        self.image_id = image_id.strip()
            
    def startVMs(self):
        self.vm_amount = int(self.vm_amount)
        self.flavor = str(self.flavor)    
        self.vm_name = self.vm_name.strip()
        
        for i in range(self.vm_amount):
            identifier = str(i)
            cmd = '/usr/bin/nova boot --flavor '+self.flavor+' --image '+self.image_id+' '+self.vm_name + "_"+ identifier
            print cmd
            if self.debug==False: print os.system(cmd)
            sys.stdout.flush() 
                   
            cmd = '/usr/bin/nova  show '+ self.vm_name + '_' + identifier
            print cmd
            if self.debug==False: print os.system(cmd)
            sys.stdout.flush()
            time.sleep(self.wait_time);
            

    def getImageIds(self):
        pattern = '\s?\|\s?([A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+).+'
        
        image_ids = list()
        s = '''+--------------------------------------+--------------------+--------+------------------------+
        |                  ID                  |        Name        | Status |        Networks        |
        +--------------------------------------+--------------------+--------+------------------------+
        | 6ac61596-0cb7-492e-ae74-ee848b1b429f | UDesktop.64        | ACTIVE | novanetwork=10.10.10.3 |
        | 98748969-f8f0-4a7f-9b1d-e07e8262fe5c | TEST_1             | ACTIVE | novanetwork=10.10.10.5 |
        | afbef7b4-a05d-469c-9432-59ecfa540a2f | UbuntuDesktopSven1 | ACTIVE | novanetwork=10.10.10.2 |
        | b79f29cf-69c3-4b3d-95ba-e676d8a847d2 | TEST_2             | ACTIVE | novanetwork=10.10.10.6 |
        | c6bb30ce-c0c2-4251-85b5-80f27b9751cc | TEST_0             | ACTIVE | novanetwork=10.10.10.4 |
        +--------------------------------------+--------------------+--------+------------------------+'''
        #print pattern
        #sys.stdout.flush() 
        s = self.listVMs()
        for line in str(s).splitlines(): # casting fuer den Fall, dass integer werte geliefert werden, dann fehlermeldung ohne cast
           #print pat.findall(line)
           match = re.search(pattern, line)
           #print "line:"+line
           if match:
               if re.search(self.vm_name+"_\d+", line):
                   image_ids.append(match.group(1))
                         
        return image_ids
        
    def listVMs(self):
        cmd = '/usr/bin/nova list'
        print cmd
        started_vms = ""
        started_vms =  os.popen(cmd).read()
        return started_vms
            
            
    def setDeleteFile(self, filename):
        self.image_id = image_id.strip()
        os.chdir(os.getcwd() + "/")
        filename = 'delete_'+self.vm_name+'-vmpool.sh'
        f = open(filename,"w+")
        content = "#!/bin/bash\n\n"
        content += "echo 'deleting corrent VMs: \n"
        matchObj = re.match("(^[A-Za-z0-9\-]).*", f, re.M|re.I)
        if matchObj: erg += f+"\n"
        try:
            for line in f:
                fileasstring += line
        finally:
            f.close()
            