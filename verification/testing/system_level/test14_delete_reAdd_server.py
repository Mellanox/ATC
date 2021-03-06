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


# pythons modules 
# local
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from alvs_infra import *
from alvs_players_factory import *

#===============================================================================
# Test Globals
#===============================================================================
request_count = 200
server_count = 10
client_count = 10
service_count = 1

#===============================================================================
# User Area function needed by infrastructure
#===============================================================================
class Test14(ALVS_Tester):
	
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
		port = '80'
		vip = self.test_resources['vip_list'][0]
		
		self.test_resources['ezbox'].add_service(vip, port)
	
		for server in self.test_resources['server_list']:
			self.test_resources['ezbox'].add_server(server.vip, port, server.ip, port)
			server.set_large_index_html()
		
		for client in self.test_resources['client_list']:
			process_list.append(Process(target=self.client_execution, args=(client,vip,)))
		for p in process_list:
			p.start()
	
		time.sleep(4)
		
		for i in range(5):		
			for server in self.test_resources['server_list'][1:]:
				print '%d: remove server: %s' %(i,server.ip)
				self.test_resources['ezbox'].delete_server(server.vip, port, server.ip, port)
			time.sleep(4)
			for server in self.test_resources['server_list'][1:]:
				print 're-add server: %s' % server.ip
				self.test_resources['ezbox'].add_server(server.vip, port, server.ip, port)
	
		for p in process_list:
			p.join()
		
		process_list = []
		for server in self.test_resources['server_list']:
			server.set_index_html(server.ip)
		
		for client in self.test_resources['client_list']:
			new_log_name = client.logfile_name+'_1'
			client.add_log(new_log_name) 
			process_list.append(Process(target=self.client_execution, args=(client,vip,)))
		for p in process_list:
			p.start()
		for p in process_list:
			p.join()
			
		print 'End user test'
	
	def run_user_checker(self, log_dir):
		print "FUNCTION " + sys._getframe().f_code.co_name + " called"
		expected_dict = {}
		expected_dict[0] = {'client_response_count':request_count,
							'client_count': client_count, 
	 						'no_404': True,
	 						'no_connection_closed': False}
		expected_dict[1] = {'client_response_count':request_count,
							'client_count': client_count, 
	 						'no_404': True,
	 						'no_connection_closed': True,
	 					 	'server_count_per_client':server_count/service_count,
	 					 	'expected_servers': self.test_resources['server_list']}
		
		if client_checker(log_dir, expected_dict, 2):
			return True
		return False
	
current_test = Test14()
current_test.main()
	
