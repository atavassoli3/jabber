#Carla Jacobsen cjacobsen2016@csu.fullerton.edu
#Spring 2021 CPSC 452 Final Project

#source: the sample codes from Dr. Gofman

# Need to run the following commands if you get errors
# pip3 uninstall pycrypto
# pip3 install -U pycryptodome

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Cipher import PKCS1_v1_5
import os

BLOCK_SIZE = 16

class myRSA(object):
    """docstring for ."""

    # default constructor
    def __init__(self, user):
        self.userName = user
        self.key = None # The symmetric key
        self.pubKey = None
        self.privKey = None
        self.keypair = (self.pubKey, self.privKey)
        self.KEY_SIZE = 512 # The maximum key size

    """
        Sets the key to use
        @param key - the key to use
        @return - True if the key is valid and False otherwise
    """
    def setKey(self, key):
        self.key = key

    """
        generates the symmetric key to use
        @param genKey - the key to generate
        @return - True if the key is valid and False otherwise
    """
    def generateKey(self):
        genKey = os.urandom(16)
        self.key = genKey
        return self.key

    """
        Sets the privKey to use
        @param privKey - the privKey to use
        @return - True if the privKey is valid and False otherwise
    """
    def setPrivKey(self, privKey):
        self.privKey = privKey

    """
        Sets the pubKey to use
        @param pubKey - the pubKey to use
        @return - True if the pubKey is valid and False otherwise
    """
    def setPubKey(self, pubKey):
        self.pubKey = pubKey

    """
        stores the keypair to use
        @param pubKey - the pubKey to use
        @param privKey - the privKey to use
        @return - True if the pubKey is valid and False otherwise
    """
    def storeKeyPair(self):
        # Generate a public/private key pair
        private_key = RSA.generate(1024)

        # Get the private key
        public_key = private_key.publickey()

        # The private key bytes to print
        privKeyBytes = private_key.exportKey(format='PEM')

        # The public key bytes to print
        pubKeyBytes = public_key.exportKey(format='PEM')

        # Save the private key
        with open (self.userName+"-pr.pem", "wb") as prv_file:
            prv_file.write(privKeyBytes)

        # Save the public key
        with open (self.userName+"-pu.pem", "wb") as pub_file:
            pub_file.write(pubKeyBytes)

    """
        loads the keypair to use
        @param pubKey - the pubKey to use
        @param privKey - the privKey to use
        @return - True if the pubKey is valid and False otherwise
    """
    def loadKeyPair(self):
        # The public key and the private key are to be stored in
        # self.pubKey and self.privKey respectively

        # Load the private key
        with open (self.userName+"-pr.pem", "rb") as prv_file:
        	contents = prv_file.read()
        	self.privKey = RSA.importKey(contents)

        # Load the public key
        with open (self.userName+"-pu.pem", "rb") as pub_file:
        	contents = pub_file.read()
        	self.pubKey = RSA.importKey(contents)

        self.keypair = (self.pubKey, self.privKey)

    """
        Encrypts a plaintext string using AES in ECB mode
        @param plaintext - the plaintext string
        @return - the encrypted ciphertext string
    """
    def encrypt(self, plaintext):

        ciphertext = ''
        # Initialize the cipher with the symmetric key and encrypt
        cipher = AES.new(self.key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), BLOCK_SIZE))
        print("Ciphertext: ", ciphertext)

        return ciphertext

    """
        Decrypts a string of ciphertext using AES in ECB mode
        @param ciphertext - the ciphertext
        @return - the plaintext
    """
    def decrypt(self, ciphertext):

        plaintext = ''

        # Initialize the cipher with the symmetric key and decrypt
        cipher = AES.new(self.key, AES.MODE_ECB)
        plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
        print("Plaintext: ", plaintext)

        return plaintext

    """
        Encrypts a symmetric key block by block using a public key
    """
    def encKey(self, plainKey):
        cipherKey  = None

        # Initialize the cipher with the key and encrypt
        cipher = PKCS1_v1_5.new(self.pubKey)
        cipherKey = cipher.encrypt(plainKey)
        print("Cipherkey: ", cipherKey)

        return cipherKey

    """
        Decrypts a symmetric key block by block using a private key
    """
    def decKey(self, cipherKey):

        plainKey  = None
        cipher = PKCS1_v1_5.new(self.privKey)
        plainKey = cipher.decrypt(cipherKey, 1000)

        return plainKey