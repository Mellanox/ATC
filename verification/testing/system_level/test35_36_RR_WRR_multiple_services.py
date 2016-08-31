#!/usr/bin/env python


#===============================================================================
# imports
#===============================================================================

# system  
import cmd
from collections import namedtuple
import logging
import os
import sys
import inspect
from multiprocessing import Process


# pythons modules 
# local
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from e2e_infra import *


#===============================================================================
# Test Globals
#===============================================================================
request_count = 1000
server_count = 12
client_count = 6
service_count = 3


#===============================================================================
# User Area function needed by infrastructure
#===============================================================================

def user_init(setup_num):
	print "FUNCTION " + sys._getframe().f_code.co_name + " called"

	service_num_servers = 4
	vip_list = [get_setup_vip(setup_num,i) for i in range(service_count)]

	index = 0
	setup_list = get_setup_list(setup_num)

	server_list=[]
	w=1
	for i in range(service_num_servers):
		server_list.append(HttpServer(ip = setup_list[index]['ip'],
						  hostname = setup_list[index]['hostname'], 
						  username = "root", 
						  password = "3tango", 
						  vip = vip_list[0],
						  eth='ens6',
						  weight=w))
		print "init server %d weight = %d" %(index,w)
		index+=1
		w+=1
	
	w=7
	for i in range(service_num_servers):
		server_list.append(HttpServer(ip = setup_list[index]['ip'],
						  hostname = setup_list[index]['hostname'], 
						  username = "root", 
						  password = "3tango", 
						  vip = vip_list[1],
						  eth='ens6',
						  weight=w))
		print "init server %d weight = %d" %(index,w)
		index+=1
		w+=4
	
	w=4
	for i in range(service_num_servers):
		server_list.append(HttpServer(ip = setup_list[index]['ip'],
						  hostname = setup_list[index]['hostname'], 
						  username = "root", 
						  password = "3tango", 
						  vip = vip_list[2],
						  eth='ens6',
						  weight=w))
		print "init server %d weight = %d" %(index,w)
		index+=1
		w+=2
	
	client_list=[]
	for i in range(client_count):
		client_list.append(HttpClient(ip = setup_list[index]['ip'],
						  hostname = setup_list[index]['hostname']))
		index+=1
	

	# EZbox
	ezbox = ezbox_host(setup_num)
	
	return (server_list, ezbox, client_list, vip_list)

def client_execution(client, vip):
	client.exec_params += " -i %s -r %d" %(vip, request_count)
	client.execute()

def run_user_test(server_list, ezbox, client_list, vip_list, sched_algorithm):
	print "FUNCTION " + sys._getframe().f_code.co_name + " called"
	process_list = []
	port = '80'

	for i in range(service_count):
		print "service %s is set with %s scheduling algorithm" %(vip_list[i],sched_algorithm)
		ezbox.add_service(vip_list[i], port, sched_alg=sched_algorithm, sched_alg_opt='')
	
	for server in server_list:
		print "adding server %s to service %s" %(server.ip,server.vip)
		ezbox.add_server(server.vip, port, server.ip, port,server.weight)
	
	print "wait 6 second for EZbox to update"
	time.sleep(6)
	
	for index, client in enumerate(client_list):
		process_list.append(Process(target=client_execution, args=(client,vip_list[index%service_count],)))
	for p in process_list:
		p.start()
	for p in process_list:
		p.join()
	
	print 'End user test'	

def run_user_checker(server_list, ezbox, client_list, log_dir,vip_list, sched_alg):
	print "FUNCTION " + sys._getframe().f_code.co_name + " called"

	sd = 0.01
	expected_dict = {'client_response_count':request_count,
						'client_count': len(client_list),
						'no_connection_closed': True,
						'no_404': True,
						'check_distribution':(server_list,vip_list,sd,sched_alg),
						'expected_servers':server_list}
	
	expected_servers = {}
	for index, client in enumerate(client_list):
		client_expected_servers=[s.ip for s in server_list if s.vip == vip_list[index%service_count]]
		expected_servers[client.ip] = client_expected_servers

	expected_dict['expected_servers_per_client'] = expected_servers
	
	return client_checker(log_dir, expected_dict)

#===============================================================================
# main function
#===============================================================================
def tests35_36_main(sched_alg):
	print "FUNCTION " + sys._getframe().f_code.co_name + " called"
	
	config = generic_main()
	
	server_list, ezbox, client_list, vip_list = user_init(config['setup_num'])
	
	init_players(server_list, ezbox, client_list, vip_list, config)
	
	run_user_test(server_list, ezbox, client_list, vip_list, sched_alg)
	
	log_dir = collect_logs(server_list, ezbox, client_list)

	gen_rc = general_checker(server_list, ezbox, client_list)
	
	clean_players(server_list, ezbox, client_list, True)
	
	user_rc = run_user_checker(server_list, ezbox, client_list, log_dir, vip_list, sched_alg)
	
	if user_rc and gen_rc:
		print 'Test passed !!!'
		exit(0)
	else:
		print 'Test failed !!!'
		exit(1)
