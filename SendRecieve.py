# import socket

# # The server port and IP
# serverIP = "127.0.0.1"
# serverPort = 1234

# Create a TCP socket that uses IPv4 address
# cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect to the server
# cliSock.connect((serverIP, serverPort))

###########################################################
# The function to handle the message of the specified format
# @param sock - the socket to receive the message from
# @returns the message without the header
############################################################


def recvMsg(sock):

    # The size
    size = sock.recv(3)

    # Convert the size to the integer
    intSize = int(size)

    # Receive the data
    data = sock.recv(intSize)

    return data


################################################
# Puts the message into the formatted form
# and sends it over the socket
# @param sock - the socket to send the message
# @param msg - the message
################################################
def sendMsg(sock, msg):

    # Get the message length
    msgLen = str(len(msg))

    # Keep prepending 0's until we get a header of 3
    while len(msgLen) < 3:
        msgLen = "0" + msgLen

    # Encode the message into bytes
    msgLen = msgLen.encode()

    # Put together a message
    sMsg = msgLen + msg.encode()

    # Send the message
    sock.sendall(sMsg)


# Send a message to the server
msg = input("Enter the user name: ")

print(type(msg))


# Send the message
sendMsg(cliSock, msg)


while True:

    msg = input("Enter a message: ")

    sendMsg(cliSock, msg)

    print(recvMsg(cliSock))

    # Send a message to the server
#	cliSock.sendall(msg.encode())

    # Receive at most 1000 bytes from the server
#	recvData = cliSock.recv(1000)

#	print(recvData)
