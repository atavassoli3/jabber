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

help_prompt = "\nClient Commands:\n" + \
"\n{who} - The server will send back the client if \nthey exist and whether they are online\n" + \
"\n{invite} [parameter] - parameter can be a list of \nusernames separated by a space. The server will \nsend symmetric keys to all of the following users \nwho are online as well as notify who was offline.\n" + \
"\n{quit} - closes the connection with the server. \nThe server will then broadcast that the user \nhas went offline to all users in the chat \nwith the same symmetric key.\n"

quit = "{quit}"
helpVar = "{help}"
invite = "{invite}"

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

        #see if there is a command
        if data == quit:
            #the user wants to quit
            # Client wants to quit
            client_socket.send(msg)
            client_socket.close()
            pass#if data == {quit}
        elif data == helpVar:
            print(help_prompt)
            pass #if data == {help}
        #source: https://stackoverflow.com/questions/663171/how-do-i-get-a-substring-of-a-string-in-python
        elif data[:len(invite)] == invite:
            #https://www.w3schools.com/python/ref_string_split.asp
            #split it into {invite} and the name of the person to invite
            inviteStr = data.split("{invite} ", 1)
            #TODO: tell the server that this client is invited
	    inviteClient(cliSock, inviteStr[1])
            pass #if data == {invite}
        else:
            #its a normal message encrypt it and send it
            encryptedData = cipher.encrypt(data.encode())
            sendMsg(cliSock, encryptedData)
            pass#else a normal message

        #old location of this code
        #encryptedData = cipher.encrypt(data.encode())
        #sendMsg(cliSock, encryptedData)


#########################################
# Waits for messages from the server and
# prints them
# @param cliSock - the socket to wait for
# the messages
#########################################
def waitForServerMsgs(cliSock):
	while True:

		msg = recvMsg(cliSock)
		print("\nReceiving === ",msg)
		#print(msg)
		
	# Send a message to the server
#	cliSock.sendall(msg.encode())

	# Receive at most 1000 bytes from the server
#	recvData = cliSock.recv(1000)

#	print(recvData)	# Create a new thread

# # Generate the public key / private key
# private_key = RSA.generate(1024)
# # Get the private key
# public_key = private_key.publickey()
# # The private key bytes to print
# privKeyBytes = private_key.exportKey(format='PEM')
# # The public key bytes to print
# pubKeyBytes = public_key.exportKey(format='PEM')

# Send the username to the server
msg = input("Enter the user name: ")
sendMsg(cliSock, msg)
print("\nSending === ",msg)
## phase 1 ##

# Load the servers public key
with open ("server-public.pem", "rb") as server_pub_file:
	contents = server_pub_file.read()
	serverPublicKey = RSA.importKey(contents)

# Load the public key
with open (msg + "-public.pem", "rb") as pub_file:
	contents = pub_file.read()
	cliPublicKey = RSA.importKey(contents)

# Load the private key
with open (msg + "-private.pem", "rb") as priv_file:
	contents = priv_file.read()
	cliPrivateKey = RSA.importKey(contents)

chatWithMsg = "symm key"
# Create a cipher based on the servers pub key
cipher = PKCS1_v1_5.new(serverPublicKey)
encryptedMsg = cipher.encrypt(msg.encode())
sendMsg(cliSock, encryptedMsg)
print("\nSending === ",encryptedMsg)
## phase 2 ##

# Receive back the encrypted sym key
encSymKey = recvMsg(cliSock)
print("\nReceiving === ",encSymKey)
## phase 3 ##	
# Decrypt to get the sym key
decryptCipher = PKCS1_v1_5.new(cliPrivateKey)
decyptedSym = decryptCipher.decrypt(encSymKey, 1000)

#print("Decrypted sym: ")
#print(decyptedSym)

# Use the sym key for the cipher
aesCipher = AES.new(decyptedSym, AES.MODE_ECB)

cipherText = aesCipher.encrypt(pad("mode".encode(), 16))

sendMsg(cliSock, cipherText)
print("\nSending === ",cipherText)
## phase 4 ##

sendThread = threading.Thread(target=waitForInput, args=(cliSock,))
recvThread = threading.Thread(target=waitForServerMsgs, args=(cliSock,))
	
# Start the thread
sendThread.start()
recvThread.start()
