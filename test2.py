#!/usr/bin/python

import os
import re
import sys
import time

def getImageIds(vm_name):

    pattern = '^\s?\|\s?([A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+).+'
    vm_name = 'TEST'       
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
    print pattern
    #sys.stdout.flush() 
    for line in s.splitlines():
       #print pat.findall(line)
       match = re.search(pattern, line)
       print line
       if match:
           print "line:"+line
           if re.search(vm_name+"_\d+", line):
               image_ids.append(match.group(1))
               print match.group(1)
               
    return image_ids


image_ids = getImageIds('TEST')
for id in image_ids:
    print id
    
pattern = '\s?\|\s?([A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+).+'
vm_name = 'TEST'       
image_ids = list()
s = '''      +--------------------------------------+--------------------+--------+------------------------+
      |                  ID                  |        Name        | Status |        Networks        |
      +--------------------------------------+--------------------+--------+------------------------+
      | 6ac61596-0cb7-492e-ae74-ee848b1b429f | UDesktop.64        | ACTIVE | novanetwork=10.10.10.3 |
      | 98748969-f8f0-4a7f-9b1d-e07e8262fe5c | TEST_1             | ACTIVE | novanetwork=10.10.10.5 |
      | afbef7b4-a05d-469c-9432-59ecfa540a2f | UbuntuDesktopSven1 | ACTIVE | novanetwork=10.10.10.2 |
      | b79f29cf-69c3-4b3d-95ba-e676d8a847d2 | TEST_2             | ACTIVE | novanetwork=10.10.10.6 |
      | c6bb30ce-c0c2-4251-85b5-80f27b9751cc | TEST_0             | ACTIVE | novanetwork=10.10.10.4 |
      +--------------------------------------+--------------------+--------+------------------------+'''
print pattern
#sys.stdout.flush() 
for line in s.splitlines():
   #print pat.findall(line)
   match = re.search(pattern, line)
   print line
   if match:
       print "line:"+line
       if re.search(vm_name+"_\d+", line):
           image_ids.append(match.group(1))
           print match.group(1) 
           
           
           
           