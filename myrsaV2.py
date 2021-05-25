#Carla Jacobsen cjacobsen2016@csu.fullerton.edu
#Spring 2021 CPSC 452 Final Project

#source: the sample codes from Dr. Gofman

# Need to run the following commands if you get errors
# pip3 uninstall pycrypto
# pip3 install -U pycryptodome

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os

#block by block decryption and encryption
BLOCK_SIZE = 8

#this class implements the rsa cipher

class myRSA(object):
    """docstring for ."""

    # default constructor
    def __init__(self, user):
        self.userName = user
        self.key = ''   #the symmetric key
        self.pubKey = ''
        self.privKey = ''
        self.keypair = (self.pubKey, self.privKey)
        # The maximum key size
        self.KEY_SIZE = 512

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
    def storeKeyPair(self):#storeKeyPair #######################################
        # Generate a public/private key pair
        private_key = RSA.generate(1024)

        # Get the private key
        public_key = private_key.publickey()

        # The private key bytes to print
        privKeyBytes = private_key.exportKey(format='PEM')


        # The public key bytes to print
        pubKeyBytes = public_key.exportKey(format='PEM')

        print("privKeyBytes = ", privKeyBytes)
        print("pubKeyBytes = ", pubKeyBytes)

        # Save the private key
        with open (self.userName+"-pr.pem", "wb") as prv_file:
            prv_file.write(privKeyBytes)

        # Save the public key
        with open (self.userName+"-pu.pem", "wb") as pub_file:
            pub_file.write(pubKeyBytes)
        pass#storeKeyPair ######################################################
    #storeKeyPair ##############################################################



    """
        loads the keypair to use
        @param pubKey - the pubKey to use
        @param privKey - the privKey to use
        @return - True if the pubKey is valid and False otherwise
    """
    def loadKeyPair(self):#loadKeyPair ##########################################
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
        #return (self.pubKey, self.privKey)
        pass#loadKeyPair #######################################################
    #loadKeyPair ###############################################################




    """
        Encrypts a plaintext string block by block
        @param plaintext - the plaintext string
        @return - the encrypted ciphertext string
    """
    def encrypt(self, plaintext):
        #call the rsa functions for encryption
        #   source:

        ciphertext = ''

        # Initielize the cipher with the key and encrypt
        cipher = PKCS1_v1_5.new(self.key)
        i = 0
        while i < len(plaintext):
            #while encrypting plaintext block by block =========================
            #block = bytes(' '.encode())

            # Read only BLOCK_SIZE number of bytes of input file
            block = bytes(plaintext[i:i + BLOCK_SIZE].encode)

            # Break if there is no more read bytes
            if(len(block) == 0):
                break

            i = i + BLOCK_SIZE

            # Pad the byte if it is less than BLOCK_SIZE number of chars
            append = (BLOCK_SIZE - len(block)) * '-'
            block = block + bytes(append.encode())

            # Encrypt the byte block
            #ciphertext = cipher.encrypt(block)
            ciphertextblock = cipher.encrypt(block, 1000)
            print("block     : ", block)
            print("ciphertext: ", ciphertextblock)

            # Write to the ciphertext
            ciphertext = ciphertext + ciphertextblock
            #done encrypting plaintext block by block ==========================

        ciphertext = cipher.encrypt(plaintext.encode())
        print("Ciphertext: ", ciphertext)

        return ciphertext
    #encrypt ###################################################################

    """
        Encrypts a symmetric key block by block using a public key
    """
    def encKey(self, plainKey):
        #call the rsa functions for encryption
        #   source:

        cipherKey  = None

        # Initielize the cipher with the key and encrypt
        cipher = PKCS1_v1_5.new(self.pubKey)
        cipherKey = cipher.encrypt(plainKey)
        print("Cipherkey: ", cipherKey)

        return cipherKey
        pass
    #encKey ####################################################################

    """
        Decrypts a symmetric key block by block using a private key
    """
    def decKey(self, cipherKey):
        #call the rsa functions for decryption
        #   source:

        plainKey  = None

        #call the rsa functions for decryption
        cipher = PKCS1_v1_5.new(self.privKey)
        plainKey = cipher.decrypt(cipherKey, 1000)
        print("Decrypted key: ", plainKey)

        return plainKey
        pass
    #decKey ####################################################################

    """
        Decrypts a string of ciphertext
        @param ciphertext - the ciphertext
        @return - the plaintext
    """
    def decrypt(self, ciphertext):
        plaintext = ''

        #call the rsa functions for decryption
        # Decrypt using the symmetric key
        cipher = PKCS1_v1_5.new(self.key)
        j = 0
        while j < len(ciphertext):
            #while decrypting ciphertext block by block ========================
            #block = bytes(' '.encode())
            # Read only BLOCK_SIZE number of bytes of input file
            block = bytes(ciphertext[j:j + BLOCK_SIZE].encode())

            # Break if there is no more read bytes
            if(len(block) == 0):
                break

            j = j + BLOCK_SIZE

            # Pad the byte if it is less than BLOCK_SIZE number of chars
            append = (BLOCK_SIZE - len(block)) * '-'
            block = block + bytes(append.encode())

            # Encrypt the byte block
            #plaintext = cipher.decrypt(block)
            plaintextblock = cipher.decrypt(block, 1000)

            print("block    : ", block)
            print("plaintext: ", plaintextblock)

            # Write to the ciphertext
            plaintext = plaintext + plaintextblock
            #done decrypting ciphertext block by block =========================
        print("Decrypted: ", plaintext)

        return plaintext
        pass
    #decrypt ###################################################################
