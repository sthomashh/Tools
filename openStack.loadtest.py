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
from Benchmark import Benchmark 

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
    wait_time = 0.0
else:
    wait_time = float(wait_time)



B1 = Benchmark()
B1.debug = 1

B1.vm_amount = vm_amount
B1.flavor = flavor
B1.vm_name = vm_name
B1.wait_time = wait_time
B1.setImageId(image_id)
B1.startVMs()


image_ids = B1.getImageIds()

for id in image_ids:
    print "nova delete "+id+"\n"








