#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os

from myrsaV2 import myRSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
#from Crypto.Cipher import PKCS1_OAEP
#from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
#from Crypto.Hash import SHA256
import binascii
import Crypto.Signature.pkcs1_15

# signature functions:
import RSAsignature
import DSAsignature

help_prompt = "\nClient Commands:\n" + \
    "\n{who} - The server will send back the client if \nthey exist and whether they are online\n" + \
    "\n{invite} [parameter] - parameter can be a list of \nusernames separated by a space. The server will \nsend symmetric keys to all of the following users \nwho are online as well as notify who was offline.\n" + \
    "\n{quit} - closes the connection with the server. \nThe server will then broadcast that the user \nhas went offline to all users in the chat \nwith the same symmetric key.\n"

clients = []
addresses = {}
inviteList = []
rsa = myRSA('server')
symmKey = rsa.generateKey()  # rsa.key is then set
print("Servers symmetric key: {}".format(symmKey))


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

    # Second interaction with client should be choosing to use DSA or not
    enable_dsa = client.recv(BUFSIZ).decode("utf8")

    if(enable_dsa == "yes"):
        clientObj.dsa = True
    else:
        clientObj.dsa = False

    # Get the clients public key from the pem file they generated
    with open(username+"-pu.pem", "rb") as pub_file:
        contents = pub_file.read()
        clientObj.pubKey = RSA.importKey(contents)

    clients.append(clientObj)

    # Encrypt the symmetric key with clients pub key
    cipher = PKCS1_v1_5.new(clientObj.pubKey)
    cipherKey = cipher.encrypt(rsa.key)
    client.send(cipherKey)
    print("Symmetric key after encrypting with clients public key: {}".format(cipherKey))

    # Welcome the user
    welcome = 'Welcome to Jabber %s! Type {help} to learn about the commands.\n' % username
    client.send(bytes(welcome, "utf8"))

    # Broadcast to other users in main chat that user is online
    msg = "%s has joined the chat!" % username
    broadcast(bytes(msg, "utf8"))

    # Handles all the messages from the client after logging in / choosing rsa or dsa
    while True:
        # For private chat rooms, this is a cross thread variable
        global inviteList

        # Attempt to receive input, if none, client has disconnected
        try:
            msg = client.recv(BUFSIZ)
            msg = rsa.decrypt(msg)
            signature = client.recv(BUFSIZ)
            signature = rsa.decrypt(signature)
            print(msg)

            if clientObj.dsa == True:
                DSAsignature.DSA_verifier(msg, signature, username)
            else:
                # msg = encodeif(msg)
                RSAsignature.verifySignature(msg, clientObj.pubKey, signature)

        except OSError:

            print("{} has disconnected".format(addresses[client]))
            break
        msg = RSAsignature.encodeif(msg)

        if(bytes("{who}", "utf8") in msg):
            client.send(bytes(getClientsOnline(clients), "utf8"))

        elif(bytes("{invite}", "utf8") in msg):
            inviteList = msg.decode().split(" ")
            inviteList[0] = username  # Removes {invite} from the inviteList
            strInviteList = ','.join(inviteList)
            # Distribute symmetric keys to all users in inviteList
            distributeSymmKeysToClients(inviteList, clients)
            msg = "Now talking in chatroom with: {}".format(strInviteList)
            broadcastToSelectClients(bytes(msg, "utf8"), inviteList, clients)

        elif(bytes("{help}", "utf8") in msg):
            client.send(bytes(help_prompt, "utf8"))

        elif(bytes("{quit}", "utf8") in msg):
            client.close()
            for c in clients:
                if(c.sock == client):
                    clients.remove(c)
            broadcast(bytes("%s has left the chat." % username, "utf8"))
        else:
            if(username in inviteList):
                broadcastToSelectClients(bytes(
                    "(Private) " + username+": " + msg.decode("utf8"), "utf8"), inviteList, clients)
            else:
                broadcast(msg, "(Global) "+username+": ")


def distributeSymmKeysToClients(inviteList, clients):
    for invite in inviteList:
        for client in clients:
            if(invite == client.username):
                key = encryptSymmKeyWithClientsPub(client.pubKey)
                client.sock.send(key)


def encryptSymmKeyWithClientsPub(pubKey):
    # Encrypt the symmetric key with clients pub key
    cipher = PKCS1_v1_5.new(pubKey)
    cipherKey = cipher.encrypt(rsa.key)
    return cipherKey


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


def broadcast(msg, prefix=""):
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
