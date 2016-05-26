#!/usr/bin/env python

import sys
sys.path.append("../")
from test_infra import *

args = read_test_arg(sys.argv)    

log_file = "dp_packet_to_host_test.log"
if 'log_file' in args:
    log_file = args['log_file']
init_logging(log_file)

scenarios_to_run = args['scenarios']

ezbox = ezbox_host(management_ip=args['host_ip'], username='root', password='ezchip',  nps_ip=args['nps_ip'], cp_app_bin=args['cp_bin'], dp_app_bin=args['dp_bin'])

if args['hard_reset']:
    ezbox.reset_ezbox(args['ezbox'])

ezbox.connect()
ezbox.terminate_cp_app()
ezbox.reset_chip()
ezbox.copy_cp_bin_to_host()
ezbox.run_cp_app()
ezbox.copy_and_run_dp_bin()

vm_management_ip = '10.137.107.5'
vm_ip = '10.7.124.2'

# connecting to a team virtual machine
vm = virtual_machine(management_ip=vm_management_ip, username='root', password='3tango', vm_ip=vm_ip)
vm.connect()

host_ip = ezbox.management_ip

####################################################################################################################
########### scenario 1: send an arp packet to the nps - packet should be send to host, not my mac ##################
####################################################################################################################

if 1 in scenarios_to_run:
    print "\nScenario 1 - Send an arp packet to the nps - packet should be send to host, not my mac"
    
    # create packet
    mac_da = 'ff ff ff ff ff ff ' # broadcast
    mac_sa = vm.mac_address.split(':')
    mac_sa = ' '.join(mac_sa) + ' '
    ether_type = '08 06 ' # arp packet type
    data = '00 01 08 00 06 04 00 01 52 54 00 c5 15 44 0a 07 7c 05 00 00 00 00 00 00 0a 07 7c 02'
    temp_str = mac_da + mac_sa + ether_type + data
    print "packet to send:\n" + temp_str
    pcap_file = 'pcap_files/arp_tmp.pcap'
    string_to_pcap_file(temp_str, pcap_file)
    print "pcap file " + pcap_file + " was created"
    
    # tcpdump to the packets on host
    cmd = 'tcpdump -G 10 -w /tmp/dump.pcap -n -i eth0:0 arp dst ' + host_ip + ' & sleep 3s && pkill -HUP -f tcpdump'
    ezbox.ssh_object.sendline(cmd)
    
    # send packet to NPS
    print "Send packet to NPS" 
    cmd = "tcpreplay --intf1=ens6 /swgwork/tomeri/sandbox/ALVS/verification/testing/dp/" + pcap_file 
    result, output = vm.execute_command(cmd)
    if result == False:
        print "Error while sending packet"
        exit(1)
     
    # read how many packets were captured
    time.sleep(5)      
    ezbox_temp = ezbox_host(hostname=host_menagement_ip, virtual_ip_address=host_ip, username='root', password='ezchip')
    ezbox_temp.connect()
    cmd = 'tcpdump -r /tmp/dump.pcap | wc -l'
    ezbox_temp.ssh_object.sendline(cmd)
    ezbox_temp.ssh_object.prompt()
    output = ezbox_temp.ssh_object.before
    output = output.strip('\r')
    output = output.split('\n')
    captured_packets = int(output[2])
    
    print "Captured " + str(captured_packets) + " Packets"   
    
    if captured_packets != 1:
        print "Error on scenario, packet wasnt sent to host"
        exit(1)
    
    # delete dump file 
    ezbox_temp.ssh_object.sendline("rm -f /tmp/dump.pcap")
    ezbox_temp.ssh_object.prompt()
    
    ezbox_temp.logout()
    del ezbox_temp
    
    print "Test Passed\n"


####################################################################################################################
############ scenario 2: send an arp packet with vlan to the nps - packet should be send to host ###################
####################################################################################################################
if 2 in scenarios_to_run:
    print "\nScenario 2 - Send an arp packet with vlan to the nps - packet should be send to host"
    
    # create packet
    mac_da = 'ff ff ff ff ff ff ' # broadcast
    mac_sa = vm.mac_address.split(':')
    mac_sa = ' '.join(mac_sa) + ' '
    ether_type = '08 06 ' # arp packet type
    vlan = '81 00 00 01'
    data = '00 01 08 00 06 04 00 01 52 54 00 c5 15 44 0a 07 7c 05 00 00 00 00 00 00 0a 07 7c 02'
    temp_str = mac_da + mac_sa + vlan + ether_type + data
    print "packet to send:\n" + temp_str
    pcap_file = 'pcap_files/arp_tmp1.pcap'
    string_to_pcap_file(temp_str, pcap_file)
    print "pcap file " + pcap_file + " was created"
    
    # tcpdump to the packets on host
    cmd = 'tcpdump -G 10 -w /tmp/dump.pcap -n -i eth0:0 arp dst ' + host_ip + ' & sleep 3s && pkill -HUP -f tcpdump'
    ezbox.ssh_object.sendline(cmd)
    
    # send packet to NPS
    print "Send packet to NPS" 
    cmd = "tcpreplay --intf1=ens6 /swgwork/tomeri/sandbox/ALVS/verification/testing/dp/" + pcap_file 
    result, output = vm.execute_command(cmd)
    if result == False:
        print "Error while sending packet"
        exit(1)
     
    # read how many packets were captured
    time.sleep(5)      
    ezbox_temp = ezbox_host(hostname=host_menagement_ip, virtual_ip_address=host_ip, username='root', password='ezchip')
    ezbox_temp.connect()
    cmd = 'tcpdump -r /tmp/dump.pcap | wc -l'
    ezbox_temp.ssh_object.sendline(cmd)
    ezbox_temp.ssh_object.prompt()
    output = ezbox_temp.ssh_object.before
    output = output.strip('\r')
    output = output.split('\n')
    captured_packets = int(output[2])
    
    print "Captured " + str(captured_packets) + " Packets"   
    
    if captured_packets != 1:
        print "Error on scenario, packet wasnt sent to host"
        exit(1)
     
    ezbox_temp.logout()
    del ezbox_temp
    
    print "Test Passed\n"



####################################################################################################################
############################### scenario 3: not udp and not tcp packet - send to host ##############################
####################################################################################################################
if 3 in scenarios_to_run:
    print "\nScenario 3 - Send an IP packet nps (multicast mac)- packet should be send to host"
    
    # create packet
#     mac_da = '01 80 C2 00 00 00 ' # broadcast
#     mac_da = '00 19 0f 25 68 aa '

    # host mac da
    mac_da = ezbox.mac_address.split(':')
    mac_da = ' '.join(mac_da) + ' '
    
    mac_sa = vm.mac_address.split(':')
    mac_sa = ' '.join(mac_sa) + ' '
    ether_type = '08 00 ' # arp packet type
    data = '45 00 00 2e 00 00 40 00 40 05 2e b6 0a 07 7c 05 0a 07 7c 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
    temp_str = mac_da + mac_sa + ether_type + data
    print "packet to send:\n" + temp_str
    pcap_file = 'pcap_files/ip_packet.pcap'
    string_to_pcap_file(temp_str, pcap_file)
    print "pcap file " + pcap_file + " was created"
    
    # tcpdump to the packets on host
    cmd = 'tcpdump -G 10 -w /tmp/dump.pcap -n -i eth0:0 dst ' + host_ip + ' & sleep 3s && pkill -HUP -f tcpdump'
    ezbox.ssh_object.sendline(cmd)
    
    # send packet to NPS
    print "Send packet to NPS" 
    cmd = "tcpreplay --intf1=ens6 /swgwork/tomeri/sandbox/ALVS/verification/testing/dp/" + pcap_file 
    result, output = vm.execute_command(cmd)
    if result == False:
        print "Error while sending packet"
        exit(1)
     
    # read how many packets were captured
    time.sleep(5)      
    ezbox_temp = ezbox_host(hostname=host_menagement_ip, virtual_ip_address=host_ip, username='root', password='ezchip')
    ezbox_temp.connect()
    cmd = 'tcpdump -r /tmp/dump.pcap | wc -l'
    ezbox_temp.ssh_object.sendline(cmd)
    ezbox_temp.ssh_object.prompt()
    output = ezbox_temp.ssh_object.before
    output = output.strip('\r')
    output = output.split('\n')
    captured_packets = int(output[2])
    
    print "Captured " + str(captured_packets) + " Packets"   
    
    if captured_packets != 1:
        print "Error on scenario, packet wasnt sent to host"
        exit(1)
     
    ezbox_temp.logout()
    del ezbox_temp
    
    print "Test Passed\n"
    
    
####################################################################################################################
############################### scenario 4: ip checksum error - send to host #######################################
####################################################################################################################
if 4 in scenarios_to_run:
    print "\nScenario 4 - scenario 4: send ip checksum error packet to host - send to host"
    
    # create packet

    # host mac da
    mac_da = ezbox.mac_address.split(':')
    mac_da = ' '.join(mac_da) + ' '
    
    mac_sa = vm.mac_address.split(':')
    mac_sa = ' '.join(mac_sa) + ' '
    ether_type = '08 00 ' # arp packet type
    data = '45 00 00 2e 00 00 40 00 40 00 2e bc 0a 07 7c 05 0a 07 7c 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
    temp_str = mac_da + mac_sa + ether_type + data
    print "packet to send:\n" + temp_str
    pcap_file = 'pcap_files/ip_checksum_error_packet.pcap'
    string_to_pcap_file(temp_str, pcap_file)
    print "pcap file " + pcap_file + " was created"
    
    # tcpdump to the packets on host
    cmd = 'tcpdump -G 10 -w /tmp/dump.pcap -n -i eth0:0 dst ' + host_ip + ' & sleep 3s && pkill -HUP -f tcpdump'
    ezbox.ssh_object.sendline(cmd)
    
    # send packet to NPS
    print "Send packet to NPS" 
    cmd = "tcpreplay --intf1=ens6 /swgwork/tomeri/sandbox/ALVS/verification/testing/dp/" + pcap_file 
    result, output = vm.execute_command(cmd)
    if result == False:
        print "Error while sending packet"
        exit(1)
     
    # read how many packets were captured
    time.sleep(5)      
    ezbox_temp = ezbox_host(hostname=host_menagement_ip, virtual_ip_address=host_ip, username='root', password='ezchip')
    ezbox_temp.connect()
    cmd = 'tcpdump -r /tmp/dump.pcap | wc -l'
    ezbox_temp.ssh_object.sendline(cmd)
    ezbox_temp.ssh_object.prompt()
    output = ezbox_temp.ssh_object.before
    output = output.strip('\r')
    output = output.split('\n')
    captured_packets = int(output[2])
    
    print "Captured " + str(captured_packets) + " Packets"   
    
    if captured_packets != 1:
        print "Error on scenario, packet wasnt sent to host"
        exit(1)
     
    ezbox_temp.logout()
    del ezbox_temp
    
    print "Test Passed\n"
    
    
    
####################################################################################################################
################## scenario 5: send a non ip packet to nps - packet should be send to host #########################
####################################################################################################################

if 5 in scenarios_to_run:
    print "\nScenario 5 - scenario 5: send a non ip packet to nps - packet should be send to host"
    
    # create packet
    mac_da = ezbox.mac_address.split(':')
    mac_da = ' '.join(mac_da) + ' '
    mac_sa = vm.mac_address.split(':')
    mac_sa = ' '.join(mac_sa) + ' '
    ether_type = '08 06 ' # arp packet type
    data = '00 01 08 00 06 04 00 01 52 54 00 c5 15 44 0a 07 7c 05 00 00 00 00 00 00 0a 07 7c 02'
    temp_str = mac_da + mac_sa + ether_type + data
    print "packet to send:\n" + temp_str
    pcap_file = 'pcap_files/arp_tmp.pcap'
    string_to_pcap_file(temp_str, pcap_file)
    print "pcap file " + pcap_file + " was created"
    
    # tcpdump to the packets on host
    cmd = 'tcpdump -G 10 -w /tmp/dump.pcap -n -i eth0:0 arp dst ' + host_ip + ' & sleep 3s && pkill -HUP -f tcpdump'
    ezbox.ssh_object.sendline(cmd)
    
    # send packet to NPS
    print "Send packet to NPS" 
    cmd = "tcpreplay --intf1=ens6 /swgwork/tomeri/sandbox/ALVS/verification/testing/dp/" + pcap_file 
    result, output = vm.execute_command(cmd)
    if result == False:
        print "Error while sending packet"
        exit(1)
     
    # read how many packets were captured
    time.sleep(5)      
    ezbox_temp = ezbox_host(hostname=host_menagement_ip, virtual_ip_address=host_ip, username='root', password='ezchip')
    ezbox_temp.connect()
    cmd = 'tcpdump -r /tmp/dump.pcap | wc -l'
    ezbox_temp.ssh_object.sendline(cmd)
    ezbox_temp.ssh_object.prompt()
    output = ezbox_temp.ssh_object.before
    output = output.strip('\r')
    output = output.split('\n')
    captured_packets = int(output[2])
    
    print "Captured " + str(captured_packets) + " Packets"   
    
    if captured_packets != 1:
        print "Error on scenario, packet wasnt sent to host"
        exit(1)
    
    # delete dump file 
    ezbox_temp.ssh_object.sendline("rm -f /tmp/dump.pcap")
    ezbox_temp.ssh_object.prompt()
    
    ezbox_temp.logout()
    del ezbox_temp
    
    print "Test Passed\n"