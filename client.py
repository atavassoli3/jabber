from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from Crypto.Cipher import AES
from myrsaV2 import myRSA

# Signature functions
import RSAsignature
import DSAsignature

cipherKey = ''  # server encrypted symmetric key with clients pub key
plainKey = ''  # symm key


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            # print(msg.decode())
            print(msg)
        except UnicodeDecodeError:  # Then we know its a cipher key if it has non utf8 chars
            cipherKey = msg
            plainKey = rsa.decKey(cipherKey)
            rsa.setKey(plainKey)
            print(plainKey)


def send(msg):
    """Handles sending of messages."""
    if msg == "{quit}":
        # Client wants to quit
        client_socket.send(msg)
        client_socket.close()
    else:
        # Encrypt the message
        client_socket.send(RSAsignature.encodeif(msg))


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    send("{quit}")


# Using Localhost as default IP and port 8000
HOST = "127.0.0.1"
PORT = "8000"
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

# Send credentials to server for verification
username = input("Enter username: ")
password = input("Enter password: ")

# Create the public and private key of the client
rsa = myRSA(username)
# Public key filename will be 'username-pu.pem'
# Private key filename will be 'username-pr.pem'
rsa.storeKeyPair()
# Now let's load those keys
# this gives us our public and private key
rsa.loadKeyPair()

enable_dsa = ''
# Send RSA or DSA choice of encryption to server
while(not("yes" in enable_dsa or "no" in enable_dsa)):
    enable_dsa = input("Enable DSA (yes or no): ")
if(enable_dsa == "yes"):
    useDSA = True
    dsa_key = DSAsignature.DSA_keyGen(username)

send("{},{}".format(username, password).encode())
send("{}".format(enable_dsa.lower()).encode())

while True:
    msg = input()
    msg = DSAsignature.encodeif(msg)
    if(useDSA):
        signature = DSAsignature.DSA_sign(msg, dsa_key)

    else:
        rsa.loadKeyPair()
        # print(type(rsa.keypair))
        signature = RSAsignature.signPlaintext(msg, rsa.privKey)
    print("Key: {}".format(rsa.key))
    msg = rsa.encrypt(msg)
    print(msg)
    send(msg)
    signature = rsa.encrypt(signature)
    send(signature)
    # send(input().encode())
