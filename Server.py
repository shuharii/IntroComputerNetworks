import socket
import EEH_constants
import json
import EEH_splitmerge
import logging

logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    ##### 2.2.0 - A
    hostedFile = input("Enter the file to host and share: ")
    #hostedfile'i parcalara ayir ve shared klasorune kaydet.
    splitmerge.splitFile(constants.SHARED_PATH, hostedFile)

    ##calisiyor dosyayi shared klasorune kopyala splitmerge orada boluyor
    # orjinal dosyayi kaldirsan iyi olur sonraki fonksiyonlarda sadece _x formati oldugu varsayiliyor cunki
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # bind to the port
    serversocket.bind((constants.HOST, constants.SERVER_PORT))

    # queue up to 5 requests
    serversocket.listen(5)


    while True:
        try:
            # establish a connection
            conn, addr = serversocket.accept()

            data = conn.recv(constants.BYTE_SIZE)
            print('request message:' + str(data.decode('utf-8')))
            request = json.loads(data.decode('utf-8'))
            print('request message:' + str(request))
            if request and "filename" in request:
                print("-" * 21 + " UPLOADING " + "-" * 21)
                # if the connection is still active we send it back the data
                # this part deals with uploading of the file
                print('requested file path:', constants.SHARED_PATH + request["filename"])
                #### 2.2.0-D
                with open(constants.SHARED_PATH + request["filename"], 'rb') as fp:
                    filechunk= fp.read(1024)
                    while filechunk:
                        conn.send(filechunk)
                        filechunk = fp.read(1024)
                print('requested file content:' + str(filechunk))
                ####2.2.0 - K
                ##### log dosyasina append yap gonderilen dosyayi `timestamp, sent to IP address, sent chunk name` formatinda
                logging.info(" " + addr[0] + ', ' + request["filename"])
                print("-" * 21 + " UPLOADED " + "-" * 21)

            conn.close()
        except Exception as e:
            print('exception: '+str(e))
