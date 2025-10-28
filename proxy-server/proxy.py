from socket import *
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
        if "\r\n\r\n".encode("utf-8") in data:
            break
    print(f'message: {message}')
    
    # Extract the filename from the given message
    try:
        #print(f'Starting File name: {message.split()[1]}')
        filename = message.split()[4]
        fileExist = False
        filetouse = filename.decode('utf-8').split(':')[0]
        
        print('File to use:', filetouse)
        # Check wether the file exist in the cache
        f = open(filetouse, "rb") # use binary mode to read the file
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
    # Error handling for file not found in cache

    except IOError:
        if fileExist == False:
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.decode('utf-8')
            print(hostn)
            file_path = message.split('/'.encode('utf-8'))[3].split()[0].decode('utf-8')
            try:
                # Connect to the socket to port 80
                # Fill in start.
                # Fill in end.
                c.connect((hostn ,80)) #need to use socket.connect() to connect to a server
                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                # [cite_start]Corrected this line based on the PDF [cite: 112-116]
                print('file_path: ', file_path)
                fileobj.write(f"GET /{file_path} HTTP/1.1\r\nHost: {hostn}\r\nConnection: close\r\n\r\n".encode('utf-8'))

                # Read the response into buffer
                # Fill in start.
                buffer = fileobj.read()
                print(f'{buffer}')
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + hostn,"wb")
                # Fill in start.
                tcpCliSock.sendall(buffer)
                tmpFile.write(buffer)
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
