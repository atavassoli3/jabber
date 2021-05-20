# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Gets the hostname of the computer
hostname = socket.gethostname()

# Gets the IP address from the hostname
IP_address = socket.gethostbyname(hostname)
  
# Statically set to work on port 8000 
Port = 8000
print(hostname, IP_address, Port)

server.connect((IP_address, Port)) 

while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [socket.socket(), server] 

    """ There are two possible input situations. Either the 
    user wants to give manual input to send to other people, 
    or the server is sending a message to be printed on the 
    screen. Select returns from sockets_list, the stream that 
    is reader for input. So for example, if the server wants 
    to send a message, then the if condition will hold true 
    below.If the user wants to send a message, the else 
    condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print(message.decode()) 
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.write("<{}}>") 
            sys.stdout.write(message) 
            sys.stdout.flush()
server.close() 