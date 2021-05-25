#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
#to generate a symmetric key
import os

#added may 22 354pm
from myrsaV2 import myRSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
#from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
#from Crypto.Hash import SHA256
import binascii
import Crypto.Signature.pkcs1_15
#end of added may 22 354pm block

help_prompt = "\nClient Commands:\n" + \
"\n{who} - The server will send back the client if \nthey exist and whether they are online\n" + \
"\n{invite} [parameter] - parameter can be a list of \nusernames separated by a space. The server will \nsend symmetric keys to all of the following users \nwho are online as well as notify who was offline.\n" + \
"\n{quit} - closes the connection with the server. \nThe server will then broadcast that the user \nhas went offline to all users in the chat \nwith the same symmetric key.\n"

clients = []
addresses = {}
inviteList = []
rsa = myRSA('server')
symmKey = rsa.generateKey() # rsa.key is then set
print(symmKey)

class Client:
	def __init__(self, sock, username, password):
		self.sock = sock
		self.username = username
		self.password = password
		self.pubKey = ''
		self.priKey = ''
		self.symKey = ''
		self.dsa = False
		self.rsa = False
	"""
		#the class members that are instances of mysignature and myrsaV2
		self.serverRSA = myRSA()

	#sets the value of the private, public, or symmetric key in the self.serverRSA member instance of the myrsaV2 class
	#call this class with the key to be stored and the mode of the key which is a string that will indicate which key is being stored
	def setMyRSAKeys(self, keyVal, keyMode):
		if keyMode == "SYM":
			#symmetric key
			self.serverRSA.key = keyVal
			pass
		elif keyMode == "PUB":
			#public key
			self.serverRSA.pubKey = keyVal
			pass
		elif keyMode == "PRI":
			#private key
			self.serverRSA.privKey = keyVal
			pass
		else:
			print("ERRROR! INVALID ARGUMENT FOR PARAMETER keyMode.")
			print("only use a string of 'SYM', 'PUB', or  'PRI', with uppercase letters only.")
			print("Your submitted string was: ", keyMode)
			pass
		pass
	"""

def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
	"""Handles a single client connection."""
	# First interaction with client should be login
	username, password = client.recv(BUFSIZ).decode("utf8").split(',')

	clientObj = Client(client, username, password)

	# Login Operation
	if(validate(username, password, clients)):
		client.send("Login Successful".encode())
	else:
		client.send("Invalid Credentials".encode())

	# Second interaction with client should be choosing to use DSA
	enable_dsa = client.recv(BUFSIZ).decode("utf8")

	if(enable_dsa == "yes"):
		clientObj.dsa = True
	else:
		clientObj.dsa = False
	
	# Get the clients public key from the pem file they generated
	with open (username+"-pu.pem", "rb") as pub_file:
		contents = pub_file.read()
		clientObj.pubKey = RSA.importKey(contents)
	
	clients.append(clientObj)	

	# Create a symmetric key 
	cipher = PKCS1_v1_5.new(clientObj.pubKey)
	cipherKey = cipher.encrypt(rsa.key)
	print(cipherKey)
	client.send(cipherKey)

	# Welcome the user
	welcome = 'Welcome to Jabber %s! Type {help} to learn about the commands.\n' % username
	client.send(bytes(welcome, "utf8"))
	
	# Broadcast to other users in main chat that user is online
	msg = "%s has joined the chat!" % username
	broadcast(bytes(msg, "utf8"))
	
	# Handles all the messages from the client after logging in / choosing rsa or dsa
	while True:
		global inviteList
		msg = client.recv(BUFSIZ)
		#decrypt the message
		msg = rsa.decrypt(msg)

		print(msg)
		if(bytes("{who}", "utf8") in msg):
			client.send(bytes(getClientsOnline(clients), "utf8"))

		elif(bytes("{invite}", "utf8") in msg):
			inviteList = msg.decode().split(" ")
			inviteList[0] = username # Removes {invite} from the inviteList
			strInviteList = ','.join(inviteList)
			msg = "Now talking in chatroom with: {}".format(strInviteList)
			broadcastToSelectClients(bytes(msg,"utf8"), inviteList, clients)

		elif(bytes("{help}", "utf8") in msg):
			client.send(bytes(help_prompt, "utf8"))

			#encrypt the message
			#ciphertext = client.serverRSA.encrypt(msg)
			#msg = ciphertext
		elif(bytes("{quit}", "utf8") in msg):
			client.close()
			for c in clients:
				if(c.sock == client):
					clients.remove(c)
			broadcast(bytes("%s has left the chat." % username, "utf8"))
		else:
			if(username in inviteList):
				broadcastToSelectClients(bytes(username+": " + msg.decode("utf8"), "utf8"), inviteList, clients)
			else:
				broadcast(msg, username+": ")

def broadcastToSelectClients(msg, inviteList, clients):
	for invite in inviteList:
		for client in clients:
			if(invite == client.username):
				client.sock.send(msg)

def getClientsOnline(clients):
	clientStr = "Online Users: "
	for client in clients:
		clientStr += client.username + ", "
	return clientStr[:-2]

def validate(username, password, clients):
	for client in clients:
		if(client.username == username and client.password != password):
			return False
	return True

def get_client(username, clients):
	for client in clients:
		if(client.username == username):
			return client
	return False

def broadcast(msg, prefix=""):  # prefix is for name identification.
	"""Broadcasts a message to all the clients."""
	for client in clients:
		client.sock.send(bytes(prefix, "utf8")+msg)


HOST = "127.0.0.1"
PORT = 8000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
	SERVER.listen(5)
	print("Waiting for connection...")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()