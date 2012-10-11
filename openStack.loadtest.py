#!/usr/bin/python
#
# @author:    Sven Thomas, sthomas@gwdg.de
        
#

import re
import os
import sys
import time
#import time


debug = 1
#####################################################################################
def startVMs(image_id, vm_amount=5, flavor=1, vm_name='TEST', wait_time=5.0):
    global debug
    vm_amount = int(vm_amount)
    flavor = str(flavor)    
    vm_name = vm_name.strip()
    
    for i in range(vm_amount):
        identifier = str(i)
        cmd = '/usr/bin/nova boot --flavor '+flavor+' --image '+image_id+' '+vm_name + "_"+ identifier
        print cmd
        if(not debug): print os.system(cmd)
        sys.stdout.flush() 
               
        cmd = '/usr/bin/nova  show '+ vm_name + '_' + identifier
        if(not debug): print os.system(cmd)
        print cmd
        sys.stdout.flush()
        time.sleep(wait_time);
        


message = 'Please give me the openrc file and path (default is /root/openrc): '
identityfile = raw_input(message+"\n:-> ").strip()
if identityfile == "":
    print "It is mandatory that you give me this information! Stopping execution of script!"
    sys.exit()
    
cmd = 'source '+identityfile    
print cmd
if(not debug): print os.system(cmd)
    
cmd = '/usr/bin/glance index'
print cmd + ":"
if(not debug): print os.system(cmd)



message = 'Please insert one image-id of an image shown below: '
image_id = raw_input(message+"\n:-> ").strip()
if image_id == "":
    print "It is mandatory that you give me an image id! Stopping execution of script!"
    sys.exit()

message = 'Please insert the whole amount of vms that shoud be startet (integer value, default is 5): '
vm_amount = raw_input(message+"\n:-> ").strip()
if vm_amount == "":
    vm_amount = 5
else:
    vm_amount = int(vm_amount)
    
    
message = 'Please insert the flavor (default is 1): '
flavor = raw_input(message+"\n:-> ").strip()
if flavor == "":
    flavor = 1
else:
    flavor = int(flavor)
    

message = 'Please insert a name-prefix for all stated vms (default is "TEST"): '
vm_name = raw_input(message+"\n:-> ").strip()
vm_name = vm_name.strip()
if vm_name == "": vm_name = "TEST"

message = 'Please insert a wait-time between the vm startups (default is 5.0 [sec]): '
wait_time = raw_input(message+"\n:-> ").strip()
if wait_time == "":
    wait_time = 5.0
else:
    wait_time = float(wait_time)

startVMs(image_id, vm_amount, flavor, vm_name, wait_time)
    







