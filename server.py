import socket
import threading
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

listenPort = 1234

# The socket the server uses for listening
listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associate the listening socket with
# port 1234
listenSock.bind(('', 1234))

# Start listening with a connection backlog queue
# of 100
listenSock.listen(100)

# The user name to socket dictionary
userNameToSockDic = {}

# A dictionary mapping user names to public keys
keyDic = {}

# The server private key
serverPrivateKey = None

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

def pubKeyExists(username):
	directories = os.listdir("./pubKeys")
	# This would print all the files and directories
	for file in directories:
		if(username.decode() in file):
			return True
	return False		


##########################################################
# Loads the public keys from the pubKey directory and 
# creates a dictionary mapping user names to public keys
# The dictionary is a globally declared keyDic dictionary
##########################################################
def loadKeys():

	# call listdir() method
	# path is a directory of which you want to list
	directories = os.listdir("./pubKeys")

	# This would print all the files and directories
	for file in directories:
	
		# Check if this is a key file
		if(file.endswith("pem")):
	
			# Load the public key
			with open ("./pubKeys/" + file, "rb") as pub_file:
	
				contents = pub_file.read()
				puKey = RSA.importKey(contents)
		
				# Get the user name from the file name
				userName = file.split("-")[0]

				# Save the user-name to key mapping in the dictionary
				keyDic[userName] = puKey	



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

############################################################
# Will be called by the thread that handles a single client
# @param clisock - the client socket
# @param userName - the user name to serve
#############################################################

def serviceTheClient(cliSock, userName):
	# Get the client's public key
	cliPubKey = keyDic[str(userName.decode())]

	#print("The key of user ", userName, " is ", cliPubKey)
	
	cipher = PKCS1_v1_5.new(serverPrivateKey)
	#cliData = recvMsg(cliSock)
	#msg = cipher.decrypt(cliData, 1000)


	# Keep servicing the client until it disconnects
	while cliSock:
		
		# Receive the data from the client
		cliData = recvMsg(cliSock)
		print("\nReceiving === ",cliData, "\n")
		## phase 2 ##	
		msg = cipher.decrypt(cliData, 1000)
		
		#print("\nGot data ", msg, " from client ", userName)
	
		randomAESKey = os.urandom(128)[:16] # Symmetric key
		#print(randomAESKey)
		cliPubKeyCipher = PKCS1_v1_5.new(cliPubKey)
		encryptedSymKey = cliPubKeyCipher.encrypt(randomAESKey)
		
		#print("encrypted sym")
		#print(encryptedSymKey)

		### Where we handle server responses to client ###

	# Send the capitalized string to the client
		for user in userNameToSockDic:
			sendMsg(userNameToSockDic[user], encryptedSymKey)
		print("\nSending === ",encryptedSymKey,"\n")
		## phase 3 ##	
		msg = recvMsg(cliSock)
		
		## phase 4 ##
		aesCipher = AES.new(randomAESKey, AES.MODE_ECB)
		
		plaintext = aesCipher.decrypt(msg)
		print("\nReceiving === ",plaintext,"\n")

	print("{} has disconnected.".format(userName))
	# Hang up the client
	cliSock.close()

# Initial loading the public keys
loadKeys()

with open ("server-private.pem", "rb") as priv_file:
	contents = priv_file.read()
	serverPrivateKey = RSA.importKey(contents)

print("Waiting for connections...")

# Server loop
while True:
	
	# Accept the connection
	clienComSock, cliInfo = listenSock.accept()
	print("New client connected: ", cliInfo)
	
	# Get the user name
	userName = recvMsg(clienComSock)
	print("\nReceiving === ",userName)	
	## phase 1 ##

	#cipher = PKCS1_v1_5.new(serverPrivateKey)
	#userName = cipher.decrypt(userName, 1000)

	#print("Got user name", userName)
	#sendMsg(clienComSock, "Welcome {}".format(userName))

	# The user name to socket	
	userNameToSockDic[userName] = clienComSock
	
	# Create a new thread
	cliThread = threading.Thread(target=serviceTheClient, args=(clienComSock,userName,))
	
	# Start the thread
	cliThread.start()