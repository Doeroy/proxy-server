from socket import *
from functools import reduce
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

HOST = sys.argv[1]
PORT = 8888
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
try: 
    tcpSerSock.bind((HOST, PORT)) #binds socket to an ip address and port
except socket.error as message:
    print('Bind failed. Error Code : ' 
          + str(message[0]) + ' Message: ' 
          + message[1])
    sys.exit()

tcpSerSock.listen(1)

# Fill in start.
# Fill in end.

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    message = b""
    while True:
        data = tcpCliSock.recv(4096)
        message += data
        if "\r\n\r\n".encode("utf-8") in message:
            break
    print(f'message: {message}')
    
    # Extract the filename from the given message
    #print(f'Starting File name: {message.split()[1]}')
    filename = message.split()[1].partition("/".encode('utf-8'))[2]
    print('------------------------------------------------------------------------')
    print(f'filename: {filename}')
    fileExist = False
    filetouse = filename.decode('utf-8')
    print('File to use:', filetouse)
    # Check wether the file exist in the cache
    print('line: 50: ', filetouse[1:].replace("/", " "))
    try:
        if filetouse in '/':
            f = open(filetouse[1:].replace("/", " "), "rb") # use binary mode to read the file
        else:
            f = open(filetouse.replace("/", " ").strip(), "rb")
        outputdata = f.read() #reads the complete file
        fileExist = True
        
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode('utf-8'))
        tcpCliSock.send("Content-Type:text/html\r\n".encode('utf-8'))
        tcpCliSock.send("\r\n".encode('utf-8'))
        # Fill in start.
        tcpCliSock.sendall(outputdata)
        # Fill in end.
        print('Read from cache')
    except IOError:
        if fileExist == False:
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = message.split()[1].split('/'.encode('utf-8'))[2].decode('utf-8')
            #hostn sshould be httpforever.com
            print('host: ', hostn)
            file_path_list = message.split()[1].split('/'.encode('utf-8'))[3:]
            print('file_path_list (L71): ', file_path_list)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                # Fill in end.
                c.connect((hostn ,80)) #need to use socket.connect() to connect to a server
                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                # [cite_start]Corrected this line based on the PDF [cite: 112-116]
                if len(file_path_list) > 1:
                    file_path = reduce(lambda x, y: x.decode('utf-8') + "/" + y.decode('utf-8'), file_path_list)
                else:
                    file_path = file_path_list[0].decode('utf-8')

                print('file_path: ', file_path)
                print('------------------------------------------------------------------------')
                fileobj.write(f"GET /{file_path} HTTP/1.1\r\nHost: {hostn}\r\nConnection: close\r\n\r\n".encode('utf-8'))
                # Read the response into buffer
                # Fill in start.
                buffer = fileobj.read()
                print(f'{buffer}')
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + hostn + " " + file_path.replace('/' , " "),"wb")
                # Fill in start.
                tmpFile.write(buffer)
                tcpCliSock.sendall(buffer)
                c.close()
                # Fill in end.
            except:
                print("Illegal request")
        else:
            print('balls')
            
    # Close the client and the server sockets
    tcpCliSock.close()
    # Fill in start.
    # Fill in end.
