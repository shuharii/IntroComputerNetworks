import EEH_constants
import socket
import json
import re

contentDictionary = dict([])

###### 2.1.0-E
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((constants.HOST, constants.LISTENER_PORT))

while True:
    ##### 2.1.0 - F
    data, addr = sock.recvfrom(constants.BYTE_SIZE)
    print("addr type:", addr[0])
    peer_ip_addr = addr[0]
    ### 2.1.0-G
    print('Received: ' + data + ' from ' + peer_ip_addr)
    # valid_json_string = "[" + data.decode('utf-8') + "]"
    userfiles = json.loads(data.decode('utf-8'))
    #### 2.1.0-H
    for file in userfiles['files']:
        if file in contentDictionary.keys():
            if (contentDictionary[file] is not None) & (peer_ip_addr not in contentDictionary[file]):
                contentDictionary[file].append(peer_ip_addr)
        else:
            ips = [peer_ip_addr]
            contentDictionary[file] = ips

    print('content dictionary:', str(contentDictionary))
    with open('contentDictionary.json', 'w') as fp:
        json.dump(contentDictionary, fp)

    #### 2.1.0 - H here ########
    # store    the    list    of    ﬁles(parsed    from the JSON    message) in a    dictionary.Let’s
    # call    this    the    content    dictionary.The    dictionary    keys    shall    be    the    content
    # chunk    name(e.g., ece    1) and the    value    shall    be    an    array    containing    the
    # list    of    IP    addresses    having    that    chunk(that    you    fetched    using    recvfrom()).This
    # dictionary    shall    be    shared    with P2P Downloader process.You may store it in a local text ﬁle
    # that is shared between the Service Listener and P2P Downloader components.
