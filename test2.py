#!/usr/bin/env python
import os
import signal

# Change this to your process name
processname = 'aterm'

for line in os.popen("ps xa"):
    fields = line.split()
    pid = fields[0]
    process = fields[4] 
    print process