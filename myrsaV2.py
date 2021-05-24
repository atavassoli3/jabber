#Carla Jacobsen cjacobsen2016@csu.fullerton.edu
#Spring 2021 CPSC 452 Final Project

#source: the sample codes from Dr. Gofman

# Need to run the following commands if you get errors
# pip3 uninstall pycrypto
# pip3 install -U pycryptodome

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

#this class implements the rsa cipher

class myrsaV2(object):
    """docstring for ."""

    # default constructor
    def __init__(self):
        self.key = None   #the symmetric key
        self.pubKey = None
        self.privKey = None
        #self.keypair = (pubKey, privKey)
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
        with open ("private.pem", "wb") as prv_file:
            prv_file.write(privKeyBytes)

        # Save the public key
        with open ("public.pem", "wb") as pub_file:
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
        with open ("private.pem", "rb") as prv_file:

        	contents = prv_file.read()
        	self.privKey = RSA.importKey(contents)


        # Load the public key
        with open ("public.pem", "rb") as pub_file:
        	contents = pub_file.read()
        	self.pubKey = RSA.importKey(contents)
        pass#loadKeyPair #######################################################
    #loadKeyPair ###############################################################




    """
        Encrypts a plaintext string
        @param plaintext - the plaintext string
        @return - the encrypted ciphertext string
    """
    def encrypt(self, plaintext):
        #call the rsa functions for encryption
        #   source:

        ciphertext = ''

        # Initielize the cipher with the symmetric key and encrypt
        cipher = PKCS1_v1_5.new(self.key)
        ciphertext = cipher.encrypt(plaintext.encode())
        print("Ciphertext: ", ciphertext)

        return ciphertext

    """
        Encrypts a symmetric key using a public key
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

    """
        Decrypts a symmetric key using a private key
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
        plaintext = cipher.decrypt(ciphertext, 1000)
        print("Decrypted: ", plaintext)

        return plaintext
        pass
