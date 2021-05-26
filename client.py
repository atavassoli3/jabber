from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import threading

# The server port and IP
serverIP = "127.0.0.1"
serverPort = 1234

# Create a TCP socket that uses IPv4 address
cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
cliSock.connect((serverIP, serverPort))

# The client private and public keys
cliPrivateKey = None
cliPublicKey = None

# Server pubic key
serverPublicKey = None

##############################################
# Encodes data only if it is not bytes
# @param data - the data
# @return encoded data if string, or the original
# data if not a string
#############################################
def encodeif(data):

    # The data
    retVal = data

    if isinstance(data, str):
        retVal = data.encode()

    return retVal



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
	sMsg = msgLen + encodeif(msg)
	
	# Send the message
	sock.sendall(sMsg)




###########################################
# A thread function that waits for the user input
# @param cliSock - the socket for sending
# data to the server
###########################################
def waitForInput(cliSock):

    while True:

        data = input("Enter something: ")
        
        encryptedData = cipher.encrypt(data.encode())
            
        sendMsg(cliSock, encryptedData)



#########################################
# Waits for messages from the server and
# prints them
# @param cliSock - the socket to wait for
# the messages
#########################################
def waitForServerMsgs(cliSock):


    while True:

        msg = recvMsg(cliSock)
	
        print("From server: ", msg)
		
	# Send a message to the server
#	cliSock.sendall(msg.encode())

	# Receive at most 1000 bytes from the server
#	recvData = cliSock.recv(1000)

#	print(recvData)	# Create a new thread


# Send a message to the server
msg = input("Enter the user name: ")

sendMsg(cliSock, msg)

print(type(msg))

# Load the public key
with open ("server-public.pem", "rb") as server_pub_file:
    contents = server_pub_file.read()
    serverPublicKey = RSA.importKey(contents)



# Load the public key
with open (msg + "-public.pem", "rb") as pub_file:
    contents = pub_file.read()
    cliPublicKey = RSA.importKey(contents)

# Load the public key
with open (msg + "-private.pem", "rb") as priv_file:
    contents = priv_file.read()
    cliPrivateKey = RSA.importKey(contents)

# Send the message
#sendMsg(cliSock, msg)

chatWithMsg = "alice darth"

# Create a cipher based on the key
cipher = PKCS1_v1_5.new(serverPublicKey)

encryptedMsg = cipher.encrypt(chatWithMsg.encode())

sendMsg(cliSock, encryptedMsg)

encSymKey = recvMsg(cliSock)

decryptCipher = PKCS1_v1_5.new(cliPrivateKey)
decyptedSym = decryptCipher.decrypt(encSymKey, 1000)

print("Decrypted sym: ")
print(decyptedSym)

aesCipher = AES.new(decyptedSym, AES.MODE_ECB)

cipherText = aesCipher.encrypt(pad("secret".encode(), 16))

sendMsg(cliSock, cipherText)


sendThread = threading.Thread(target=waitForInput, args=(cliSock,))
recvThread = threading.Thread(target=waitForServerMsgs, args=(cliSock,))
	
# Start the thread
#sendThread.start()
#recvThread.start()
