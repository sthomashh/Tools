#!/usr/bin/python
#
# Loadtest for OpenStack cloud:
#
# Creates a lot  of VMs...
#
# @author:  Piotr Kasprzak, piotr.kasprzak@gwdg.de

import httplib
import json
import sys
import logging
import time
import uuid

os_controller		= "141.5.97.1"

keystone_endpoint	= os_controller + ":35357"
nova_endpoint		= os_controller + ":8774"

user        		= "admin"
tenant      		= "openstack"
password    		= "0p3nst4ck!"

# Flavor to use
flavor 				= "m1.micro"

# Image to use
#image 				= "Ubuntu.12.04.LTS.Server.64bit.img"
image 				= "Ubuntu 12.10 Server x64"

# VM name prefix
vm_name_prefix		= "loadtest-vm-"

# Number of VMs being spawed concurrently
pending_vms 		= 5

# Maximum number of VMs to spawn
max_vms				= 50

headers	= {"Content-Type":	"application/json"}

# Initialize logging

# create logger
log = logging.getLogger('loadtest')
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)

def do_rest_call(endpoint, uri, method, params):

	log.debug("Request %s@%s:%s :: %s" % (method, endpoint, uri, params))

	json_params = None
	if params:
		json_params = json.dumps(params)

	con = httplib.HTTPConnection(endpoint)
	con.request(method, uri, json_params, headers)

	response	= con.getresponse()
	json_data	= response.read()
	data 		= None
	if json_data:
		data 	= json.loads(json_data)

	con.close()

	log.debug("%s: %s :: %s" % (response.status, response.reason, json_data))

	return data

def authenticate(tenant, user, password):

	log.info("Authenticating against keystone...")

	# Build hash for keystone auth request
	params = {}
	params['auth'] = {}
	params['auth']['passwordCredentials'] = {}
	params['auth']['passwordCredentials']['username'] = user
	params['auth']['passwordCredentials']['password'] = password
	params['auth']['tenantName'] = tenant

	auth_data = do_rest_call(keystone_endpoint, "/v2.0/tokens", "POST", params)

	data = {}
	data['token_id']	= auth_data['access']['token']['id']
	data['tenant_id']	= auth_data['access']['token']['tenant']['id']

	log.info("Token-id:  %s" % data['token_id'])
	log.info("Tenant-id: %s" % data['tenant_id'])

	return data

def get_flavor_id(flavor):

	log.info("Resolving flavor '%s'" % flavor)

	flavors_data = do_rest_call(nova_endpoint, "/v2/%s/flavors" % tenant_id, "GET", None)

	flavor_id = -1
	for flavor_entry in flavors_data['flavors']:
		if flavor_entry['name'] == flavor:
			flavor_id = flavor_entry['id']
			break;

	if flavor_id == -1:
		raise Exception("Could not resolve flavor-id of flavor '%s'!" % flavor)

	log.info("Flavor-id: %s" % flavor_id)

	return flavor_id

def get_image_id(image):

	log.info("Resolving image '%s'" % image)

	images_data = do_rest_call(nova_endpoint, "/v2/%s/images" % tenant_id, "GET", None)

	image_id = -1
	for image_entry in images_data['images']:
		if image_entry['name'] == image:
			image_id = image_entry['id']
			break;

	if image_id == -1:
		raise Exception("Could not resolve image-id of image '%s'!" % image)

	log.info("Image-id: %s" % image_id)

	return image_id

def instantiate_vm(tenant_id, flavor_id, image_id):

	log.info("Instantiating VM...")

	params = {}
	params['server'] = {}
	params['server']['flavorRef']	= flavor_id
	params['server']['imageRef']	= image_id
	params['server']['name']		= vm_name_prefix + str(uuid.uuid4())

	vm_data = do_rest_call(nova_endpoint, "/v2/%s/servers" % tenant_id, "POST", params)

	vm_id = vm_data['server']['id']

	log.info("VM created: %s" % vm_id)

	return vm_id

def delete_vm(tenant_id, vm_id):

	log.info("Deleting vm '%s'..." % vm_id)

	do_rest_call(nova_endpoint, "/v2/%s/servers/%s" % (tenant_id, vm_id), "DELETE", None)

def get_vm_details(tenant_id, vm_id):

	log.info("Getting details for vm '%s'" % vm_id)

	vm_data = do_rest_call(nova_endpoint, "/v2/%s/servers/%s" % (tenant_id, vm_id), "GET", None)

	return vm_data

def get_vms_by_name(tenant_id, name):

	log.info("Getting all vms containing '%s' in the name..." % name)

	vms_data = do_rest_call(nova_endpoint, "/v2/%s/servers" % tenant_id, "GET", None)

	log.info("Found [%d] vms" % len(vms_data['servers']))

	vm_ids = []
	for vm_entry in vms_data['servers']:
		log.debug("Checking vm '%s'..." % vm_entry['name'])
		if name in vm_entry['name']:
			log.debug(". adding")
			vm_ids.append(vm_entry['id'])

	log.info("[%d] vms match criteria" % len(vm_ids))

	return vm_ids

def instantiate_lots_of_vms(tenant_id):

	log.info("Instantiating [%d] vms..." % max_vms)

	instantiate_credit = pending_vms
	instantiated_vm_ids = []
	i = 0

	while i < max_vms:

		# Determine number of vms that can be instantiated in current step
		if max_vms - i >= instantiate_credit:
			vms_to_instantiate_count = instantiate_credit
		else:
			vms_to_instantiate_count = max_vms - i

		# Batch instantiate vms
		while vms_to_instantiate_count > 0:
			vm_id = instantiate_vm(tenant_id, flavor_id, image_id)
			i = i + 1
			vms_to_instantiate_count = vms_to_instantiate_count - 1
			instantiated_vm_ids.append(vm_id)
			log.info("* * * Instantiated vm %d (%s) * * *" % (i, vm_id))

		# Wait for at least one instantiation having finished
		while 1:
			time.sleep(1)
			# Check instantiation status for all pending instantiations
			for vm_id in instantiated_vm_ids:
				vm_details = get_vm_details(tenant_id, vm_id)
				if vm_details['server']['status'] == "ACTIVE":
					log.info("vm '%s' is active!" % vm_id)
					instantiated_vm_ids.remove(vm_id)
			# At least one vm finished being deleted
			if len(instantiated_vm_ids) < pending_vms:
				instantiated_credit = pending_vms - len(instantiated_vm_ids)
				break	

	return

def delete_vms_by_name(tenant_id, name):

	vm_ids = get_vms_by_name(tenant_id, name)
	log.info("Deleting [%d] vms..." % len(vm_ids))

	delete_credit = pending_vms
	deleted_vm_ids = []
	i = 0

	while len(vm_ids) > 0:

		# Determine number of vms to be deleted in one step
		if len(vm_ids) >= delete_credit:
			vms_to_delete_count = delete_credit
		else:
			vms_to_delete_count = len(vm_ids)

		# Batch delete vms
		while vms_to_delete_count > 0:
			vm_id = vm_ids.pop(0)
			i = i + 1
			log.info("Deleting vm %d (%s)" % (i, vm_id))
			vms_to_delete_count = vms_to_delete_count - 1
			deleted_vm_ids.append(vm_id)
			delete_vm(tenant_id, vm_id)

		# Wait for at least one delete having finished
		while 1:
			time.sleep(1)
			# Check delete status for all pending deletes
			for vm_id in deleted_vm_ids:
				vm_details = get_vm_details(tenant_id, vm_id)
				if vm_details.has_key('itemNotFound'):
					log.info("vm '%s' has been deleted!" % vm_id)
					deleted_vm_ids.remove(vm_id)
			# At least one vm finished being deleted
			if len(deleted_vm_ids) < pending_vms:
				delete_credit = pending_vms - len(deleted_vm_ids)
				break
	return


auth_data = authenticate(tenant, user, password)

token_id 	= auth_data['token_id']
tenant_id 	= auth_data['tenant_id']

headers['X-Auth-Token'] = token_id

# Get flavor id
flavor_id = get_flavor_id(flavor)

# Get image id
image_id = get_image_id(image)

# Create VMs
#instantiate_lots_of_vms(tenant_id)

# Delete vms
delete_vms_by_name(tenant_id, vm_name_prefix)

# Finished
log.info("* * * * * Finished! * * * * *")

sys.exit(0)

#vm_id = instantiate_vm(tenant_id, flavor_id, image_id)

#i = 0
#while 1:
#	time.sleep(1)
#	vm_details = get_vm_details(tenant_id, vm_id)
#	log.debug("VM state: %s" % vm_details['server']['status'])
#	if vm_details['server']['status'] == "ACTIVE":
#		log.info("*** Finished ***")
#		break 

#vm_ids = get_vms_by_name(tenant_id, vm_name_prefix)

#delete_vm(tenant_id, vm_id)

# Check status
#while 1:
#	time.sleep(1)
#	vm_details = get_vm_details(tenant_id, vm_id)
#	if vm_details.has_key('itemNotFound'):
#		log.info("*** Finished ***")
#		break 
#	else:
#		log.debug("VM state: %s" % vm_details['server']['status'])

