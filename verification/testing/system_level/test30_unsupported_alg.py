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
from alvs_tester_class import ALVS_Tester
from alvs_players_factory import *

# pythons modules 
# local
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from alvs_infra import *


#===============================================================================
# Test Globals
#===============================================================================
request_count = 10
server_count = 5
client_count = 1
service_count = 1



#===============================================================================
# User Area function needed by infrastructure
#===============================================================================
class Test30(ALVS_Tester):
	
	def user_init(self, setup_num):
		print "FUNCTION " + sys._getframe().f_code.co_name + " called"
		
		self.test_resources = ALVS_Players_Factory.generic_init(setup_num, service_count, server_count, client_count)
		
		for s in self.test_resources['server_list']:
			s.vip = self.test_resources['vip_list'][0]
	
	def client_execution(self, client, vip):
		client.exec_params += " -i %s -r %d" %(vip, request_count)
		client.execute()
	
	def run_user_test(self):
		print "FUNCTION " + sys._getframe().f_code.co_name + " called"
		process_list = []
		ezbox = self.test_resources['ezbox']
		server_list = self.test_resources['server_list']
		client_list = self.test_resources['client_list']
		vip = self.test_resources['vip_list'][0]
		port = '80'
	
		ezbox.add_service(vip, port, sched_alg='lc' ,sched_alg_opt='')
		for server in server_list:
			ezbox.add_server(vip, port, server.ip, port)
		
		
		for client in client_list:
			process_list.append(Process(target=self.client_execution, args=(client,vip,)))
		for p in process_list:
			p.start()
		for p in process_list:
			p.join()
		
		print 'End user test'
	
	def run_user_checker(self, log_dir):
		print "FUNCTION " + sys._getframe().f_code.co_name + " called"
		expected_dict= {'client_response_count':request_count,
						'client_count': client_count, 
						'no_404': True,
						'no_connection_closed': True,
						'server_count_per_client':server_count}
		
		return client_checker(log_dir, expected_dict)
	
current_test = Test30()
current_test.main()
