import socket
import time
import EEH_constants
import json
import sys
import EEH_splitmerge
import logging
import os

logging.basicConfig(filename='downloader.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

def isAllDownloaded(requestedFile):
    dirfiles = os.listdir(constants.SHARED_PATH)
    for i in range(1, 6):
        if requestedFile+"_"+str(i) not in dirfiles:
            return False

    return True


def fetch(addr, request):
    try:
        # set up socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow python to use recently closed socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # make the connection
        s.connect((addr, constants.SERVER_PORT))

        print('requested file name:', str(json.dumps(request)))
        s.send(json.dumps(request).encode('utf-8'))


        print("Recieving -------")
        buffer = b""
        while True:
            data = s.recv(constants.BYTE_SIZE)
            if not data:
                break
            buffer += data
        print("\nRecieved file on the client side is:")

        ##### 2.2.0 - I
        s.close()
        return buffer
    except Exception as e:
        print("exception: "+ str(e))
        sys.exit()




if __name__ == "__main__":


    while True:
        ##### 2.2.0 - E
        requestedFile = input("Enter the file to request: ")

        req = dict([])

        ##### 2.2.0-F
        with open('contentDictionary.json', 'r') as fp:
            contentDictionary = json.load(fp)
        # ###### 2.2.0 - G birden fazla hostta ayni content olabilir asagidaki kodun sadece birincisini aldigini sabitlemek iyi olur.
        # {"eren_2": ["192.168.0.101"], "eren_1": ["192.168.0.101"],
        #  "eren_5": ["192.168.0.101"], "adele_4": ["192.168.0.111", "192.168.0.101"],"adele_2": ["192.168.0.111", "192.168.0.101"],
        #  "adele_1": ["192.168.0.111", "192.168.0.101"], "adele_3": ["192.168.0.111", "192.168.0.101"], "eren_4": ["192.168.0.101"],
        #  "adele_5": ["192.168.0.111", "192.168.0.101"], "eren_3": ["192.168.0.101"]}
        for i in range(1, 6):
            try:
                for host in contentDictionary[requestedFile+"_"+str(i)]:
                    #### 2.2.0-H
                    req['filename'] = requestedFile+"_"+str(i)
                    ##### 2.2.0 - E
                    print("requesting " + requestedFile + "_" + str(i) + " from " + host)
                    data = fetch(host, req)
                    print("ip address for "+requestedFile+"_"+str(i)+" is " + host)

                    with open(constants.SHARED_PATH+requestedFile+"_"+str(i), 'wb') as infile:
                        infile.write(data)
                    ####2.2.0 - L
                    ##### log dosyasina append yap alinan dosyayi `timestamp, chunk name, downloaded from IP address` formatinda
                    logging.info(" "+requestedFile+"_"+str(i)+', ' + host)
            except KeyError as e:
                #### sadece key hatasina bakiyor yani distionary de yoksa baglanti sonucu gelmedigi takdirde try except ile de kontrol gerekiyor.
                #### fetch(host, req) fonksiyonuna hata firlatmasi yapilabilir ya da o fonksiyonun icin de hata verdirilebilir.
                print("There is no host to serve " + requestedFile + "_" + str(i))

        ###### 2.2.0-J
        # check all    5    chunks    have     been    downloaded.After the    5th chunk has been  downloaded, P2PDownloader shall
        # combine these 5 chunks  into a single ﬁle.(I’ll provide   the  code for this, which you’ll integrate in your P2P Downloader code.)
        # Once the ﬁle is ready, the P2P Downloader shall inform the user via the terminal that the ﬁle has been successfully downloaded.
        ###### Buraya bir kontrol kodu yaz asagidakini de birlestirmek icin kullanabilirsin
        ###### splitmerge.mergeFile(constants.SHARED_PATH, requestedFile)
        if isAllDownloaded(requestedFile):
            splitmerge.mergeFile(constants.SHARED_PATH, requestedFile)
        else:
            print("Not all chunks of " + requestedFile + " have been completed")

    ##### 2.2.0 - M server surekli calisiyor burayi da surekli calisir hale getirmek gerekiyor...
