#!/usr/bin/python
#
# @author:    Sven Thomas, sthomas@gwdg.de

import os
import logging

class TestDeamons: 
    debug = False
    deamons = list()
    debug_filehandler = logging.ERROR
    debug_console     = logging.CRITICAL
    log = None
    
    def __init__(self):
        self.__setLogging()
        
    
        
    def setDeamon(self, param):
        
        self.deamons.append(param)   
        self.log.info("added param:  %s" % param)
        
        
    def startTest(self):
         for deamon in self.deamons:
             #print deamon
             cmd = "ps aux|egrep -i "+deamon+"|wc -l"
             self.log.debug("execute command:  %s" % cmd)
             test = int(os.popen(cmd).read())
             #self.log.debug("test:  %s" % test)
             if test<=2:
                 self.log.critical("Not running :  %s" % deamon)
             else:
                 self.log.info("Running :  %s" % deamon)
                 print "Running :  %s" % deamon
                 
    
    def __setLogging(self):
        # Initialize logging
        # create logger
        self.log = logging.getLogger('test_deamons')
        self.log.setLevel(self.debug_console)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('test_deamons.log')
        fh.setLevel(self.debug_filehandler)
         # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(self.debug_console)       
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s') 
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.log.addHandler(fh)
        self.log.addHandler(ch)



# Run Deamon-Test:
folsom = False
type = "cloud-controller"
#type = "compute-node"
#type = "all"

TD1 = TestDeamons()

if type == "cloud-controller":
    print "\nTest deamons on Openstack Cloud Controller installation:\n"
    TD1.setDeamon("keystone")
    TD1.setDeamon("glance-api")
    TD1.setDeamon("glance-registry")
    TD1.setDeamon("nova-cert")      
    TD1.setDeamon("nova-api")
    TD1.setDeamon("nova-objectstore")
    TD1.setDeamon("nova-scheduler")
    TD1.setDeamon("nova-volume")
    TD1.setDeamon("novnc")
    TD1.setDeamon("nova-consoleauth")
    TD1.setDeamon("mysql")
    TD1.setDeamon("rabbitmq")

if type == "compute-node":
    print "\nTest deamons on Openstack Compute Node installation:\n"
    TD1.setDeamon("libvirtd")
    TD1.setDeamon("nova-compute")
    TD1.setDeamon("nova-network")

if type == "all":
    print "\nTest deamons on Openstack ALL in One installation:\n"
    TD1.setDeamon("keystone")    
    TD1.setDeamon("glance-api")
    TD1.setDeamon("glance-registry")
    TD1.setDeamon("libvirtd")
    TD1.setDeamon("nova-compute")
    TD1.setDeamon("nova-network")
    TD1.setDeamon("nova-cert")      
    TD1.setDeamon("nova-api")
    TD1.setDeamon("nova-objectstore")
    TD1.setDeamon("nova-scheduler")
    TD1.setDeamon("nova-volume")
    TD1.setDeamon("novnc")
    TD1.setDeamon("nova-consoleauth")
    TD1.setDeamon("mysql")
    TD1.setDeamon("rabbitmq")

if folsom==True:
    TD1.setDeamon("quantum")

TD1.startTest()