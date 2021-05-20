

#source: the sample codes from Dr. Gofman

from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
import Crypto.Signature.pkcs1_15

class mysignature(object):
    """docstring for ."""

    # default constructor
    def __init__(self):
        self.key = ''
        self.pubKey = ''
        self.privKey = ''

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
        # Generate a keypair TODO

        #got the keys now save them to the object
        self.setPubKey(self, pubKey)
        self.setPrivKey(self, privKey)
        pass#setKeyPair ########################################################
    #setKeyPair ################################################################

    """
        Encrypts a plaintext string
        @param plaintext - the plaintext string
        @return - the encrypted ciphertext string
    """
    def encrypt(self, plaintext):
        #call the signature functions for encryption
        #   source:

        ciphertext = ''

        #call the signature functions for encryption    TODO

        return ciphertext

    """
        Encrypts a symmetric key
    """
    def encKey(self):
        #call the signature functions for encryption
        #   source:

        cipherKey  = ''

        #call the signature functions for encryption    TODO

        return cipherKey
        pass

    """
        Decrypts a symmetric key
    """
    def decKey(self):
        #call the signature functions for decryption
        #   source:

        plainKey  = ''

        #call the signature functions for decryption    TODO

        return plainKey
        pass

    """
        Decrypts a string of ciphertext
        @param ciphertext - the ciphertext
        @return - the plaintext
    """
    def decrypt(self, ciphertext):
        plaintext = ''

        #call the signature functions for decryption    TODO

        return plaintext
        pass
