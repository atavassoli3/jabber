#Carla Jacobsen cjacobsen2016@csu.fullerton.edu
#Spring 2021 CPSC 452 Final Project

#source: the sample codes from Dr. Gofman

import rsa
import sys
from rsa import key, common

#this class implements the rsa cipher

class myrsa(object):
    """docstring for ."""

    # default constructor
    def __init__(self):
        self.key = ''   #the symmetric key
        self.pubKey = ''
        self.privKey = ''
        self.keypair = (pubKey, privKey)
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
        Sets the keypair to use
        @param pubKey - the pubKey to use
        @param privKey - the privKey to use
        @return - True if the pubKey is valid and False otherwise
    """
    def setKeyPair(self):#setKeyPair ###########################################
        # Generate a keypair. The key size is 512 bits
        (pubKey, privKey) = self.rsa.newkeys(self.KEY_SIZE, accurate=True)

        #got the keys now save them to the object
        self.setPubKey(self, pubKey)
        self.setPrivKey(self, privKey)
        pass#setKeyPair ########################################################
    #setKeyPair ################################################################

    """
        grabs the message from the user
        calls the encrypt function
        calls the decrypt function
    """
    #unsure if using this function or not
    #def handleMesg(self, argv):#handleMesg #####################################
        #handleMesg ############################################################
        #grab the message from the user ========================================
        # Make sure the user provided plaintext to encrypt
        #if len(sys.argv) < 2:
        #	print "USAGE: ", sys.argv[0], "'<plaintext>'"
        #	exit(-1)

        # Grab the plaintext
        #plaintext = sys.argv[1]

        # The cipher text
        #ciphertext = ""

        # The decrypted text
        #decryptedText = ""

        #Generate a new keypair
        #self.setKeyPair(self)

        # Make sure the length of the plaintext does not exceed the
        # the length of the cipher text.
        # Catch: 11 bytes of the plaintext buffer used by RSA
        # library are always reerved for padding. Hence, the maximum
        # plaintext size that can be handled at once is: modulus size in bytes - 11
        #if len(sys.argv[1]) > common.byte_size(self.pubKey.n) - 11:
        #	print("The text of size ", len(sys.argv[1]),  "Exceeds maximum size of ", common.byte_size(self.pubKey.n) -11)
        #	exit(-1)
        #done with grab the message from the user ==============================

        #encrypt ===============================================================
        #ciphertext = self.encrypt(self, plaintext)
        # done with encrypt ====================================================

        #decrypt ===============================================================
        #plaintext = self.decrypt(self, ciphertext)
        #done with decrypt =====================================================


        #handleMesg ############################################################
        #pass#handleMesg ########################################################
    #handleMesg ################################################################



    """
        Encrypts a plaintext string
        @param plaintext - the plaintext string
        @return - the encrypted ciphertext string
    """
    def encrypt(self, plaintext):
        #call the rsa functions for encryption
        #   source:

        ciphertext = ''

        #call the rsa functions for encryption
        # Encrypt using the symmetric key
        ciphertext = self.rsa.encrypt(plaintext, self.key)

        return ciphertext

    """
        Encrypts a symmetric key using a public key
    """
    def encKey(self, key):
        #call the rsa functions for encryption
        #   source:

        cipherKey  = ''

        #call the rsa functions for encryption
        ciphertext = self.rsa.encrypt(plaintext, self.pubKey)

        return cipherKey
        pass

    """
        Decrypts a symmetric key using a private key
    """
    def decKey(self, cipherkey):
        #call the rsa functions for decryption
        #   source:

        plainKey  = ''

        #call the rsa functions for decryption
        plainKey = self.rsa.decrypt(ciphertext, self.privKey)

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
        # Decrypt using the private key
        decryptedText = self.rsa.decrypt(ciphertext, self.key)

        return plaintext
        pass
