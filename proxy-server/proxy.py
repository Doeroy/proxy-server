from socket import *
from functools import reduce
import sys
import os

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

HOST = sys.argv[1]
PORT = 8888
tcpSerSock = socket(AF_INET, SOCK_STREAM)
try: 
    tcpSerSock.bind((HOST, PORT)) 
except socket.error as message:
    print('Bind failed. Error Code : ' 
          + str(message[0]) + ' Message: ' 
          + message[1])
    sys.exit()

tcpSerSock.listen(1)

while 1:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept() 
    print('Received a connection from:', addr)
    message = b""
    while True: #recieves all the data from the user and adds it to message
        data = tcpCliSock.recv(4096)
        message += data
        if "\r\n\r\n".encode("utf-8") in message:
            break
    print(f'message: {message.decode('utf-8')}')
    filename = message.split()[1].partition("/".encode('utf-8'))[2].decode('utf-8').strip('/')
    print('------------------------------------------------------------------------')
    print(f'filename: {filename}')
    fileExist = False
    filetouse = "/" + filename.replace('/', " ") #replaces slashes with spaces for file names
    print('File to use:', filetouse)
    try:
        f = open(filetouse[1:], "rb")
        outputdata = f.read()
        f.close()
        fileExist = True
        tcpCliSock.sendall(outputdata)
        print('Read from cache')
    except IOError:
        if fileExist == False:
            c = socket(AF_INET, SOCK_STREAM)
            #li contains the hostname and potenial file paths
            li = filename.replace("www.","",1).rstrip('/').split('/', 1) 
            hostn = li[0]
            if len(li) > 1: 
                file_path = li[1]
            else:
                file_path = ''
            print('hostn: ', hostn)
            print('file_path ', file_path)
            try:
                #created an additonal socket to communicate with the webpage
                c.connect((hostn ,80)) 
                fileobj = c.makefile('rwb', 0)
                print('------------------------------------------------------------------------')
                fileobj.write(f"GET /{file_path} HTTP/1.0\r\nHost: {hostn}\r\nConnection: close\r\n\r\n".encode('utf-8'))
                #reads the message obtained from the get request and puts it into a buffer
                #that sends message to the user
                buffer = fileobj.read()
                print(f'{buffer}')
                tcpCliSock.sendall(buffer)
                c.close()
                try:
                    #creates the new file name for the file
                    cache_path = "./" + filetouse
                    cache_dir = os.path.dirname(cache_path)
                    #if the directory does not exist then we create it
                    if cache_dir and not os.path.exists(cache_dir):
                        os.makedirs(cache_dir)
                    #create the new file and write the message that is inside the buffer
                    tmpFile = open(cache_path, "wb")
                    tmpFile.write(buffer)
                    tmpFile.close()
                    print('Cached successfully')
                except Exception as cache_error:
                    print(f'Failed to cache file: {cache_error}')
                    
            except Exception as e:
                print(f'Error fetching from server: {e}')
                tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode('utf-8'))
                tcpCliSock.send("Content-Type:text/html\r\n".encode('utf-8'))
                tcpCliSock.send("\r\n".encode('utf-8'))
                tcpCliSock.send("<html><body><h1>404 Not Found</h1></body></html>".encode('utf-8'))
                try:
                    c.close()
                except:
                    pass
        else:
            print('balls')
            
    tcpCliSock.close()
   