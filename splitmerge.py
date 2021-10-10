import os
import math
import EEH_constants


def splitFile(file_path, content_name):
    #content_name = 'py'  # This'll be the parameter you provide for this code. The name of the content that the user wants to download.

    filename = file_path + content_name + '.png'
    print("path:", filename)
    c = os.path.getsize(filename)
    # print(c)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
    # print(CHUNK_SIZE)

    index = 1
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = file_path + content_name + '_' + str(index)
            # print("chunk name is: " + chunkname + "\n")
            with open(chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
        chunk_file.close()

####################################################################################


# STITCH IMAGE BACK TOGETHER
# # Normally this will be in another location to stitch it back together
def mergeFile(file_path, content_name):
    #content_name = 'py'  # again, this'll be the name of the content that used wanted to download from the network.
    chunknames = [content_name + '_1', content_name + '_2', content_name + '_3', content_name + '_4', content_name + '_5']

    # with open(content_name+'.png', 'w') as outfile:
    with open(file_path + content_name+'.png', 'wb') as outfile:  # in your code change 'ece.png' to content_name+'.png'
        for chunk in chunknames:
            with open(file_path+chunk,'rb') as infile:
                outfile.write(infile.read())



if __name__ == "__main__":
    hostedFile = input("Enter the file to host and share: ")
    splitFile(constants.SHARED_PATH, hostedFile)
