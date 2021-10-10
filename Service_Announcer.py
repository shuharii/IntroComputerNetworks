import ipaddress

import EEH_constants
import socket
import time
import os
import json

#####  2.1.0-A
####### Write a prompt to get user name and store in json instead of "ece" #########
username = input("Enter your user name: ")



###### 2.1.0-E
####### Get host IP address and Net Mask  from Network Interface and calculate broadcast ip address #####

# ## getting the hostname by socket.gethostname() method
# hostname = socket.gethostname()
# ## getting the IP address using socket.gethostbyname() method
# ip_address = socket.gethostbyname(hostname)
# mask = '255.255.255.0'
#
#
#
# host = ipaddress.IPv4Address(ip_address)
# net = ipaddress.IPv4Network(ip_address + '/' + mask, False)
# # print('IP:', IP)
# # print('Mask:', MASK)
# # print('Subnet:', ipaddress.IPv4Address(int(host) & int(net.netmask)))
# # print('Host:', ipaddress.IPv4Address(int(host) & int(net.hostmask)))
# # print('Broadcast:', net.broadcast_address)
#
#
# # Get the current host ip and net mask using some other library or os function
# # Assuming ip and mask is below implement codes below
# # IP = '192.168.0.16'
# # MASK = '255.255.255.0'
# #
# # host = ipaddress.IPv4Address(IP)
# # net = ipaddress.IPv4Network(IP + '/' + MASK, False)
# # print('IP:', IP)
# # print('Mask:', MASK)
# # print('Subnet:', ipaddress.IPv4Address(int(host) & int(net.netmask)))
# # print('Host:', ipaddress.IPv4Address(int(host) & int(net.hostmask)))
# print('Broadcast:', net.broadcast_address)




# create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


#####2.1.0-D
####### Read files from shared folder and create json array ####
files = os.listdir(constants.SHARED_PATH)
files = [n for n in files if ("." not in n) & ("_" in n)]
print('files:', str(files))

###### 2.1.0-C

### "files": [ "ece_1", "ece_2", "ece_3", "ali_2", "ayse_1", "cem_1", "cem_2"] #####
message = dict([])
message["username"] = username
message["files"] = files
#print('message:', str(message))

##### 2.1.0-B
while True:
    sock.sendto(json.dumps(message).encode('utf-8'), ("192.168.1.255", constants.LISTENER_PORT))
    time.sleep(60)
