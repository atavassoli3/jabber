

# source: the sample codes from Dr. Gofman

from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
import Crypto.Signature.pkcs1_15

# 1. need to import the appropriate class to supply the user's  keypair

# ======================================================
# 2. keyPair needs to be passed to this function for signing -
# what is the format of the keyPair and which function passes it?
# some options are: store in the database, .pem file
# 3. the function converts plaintext to bytes
"""
    Sign plaintext with RSA keyPair
    @param key - the key to use
    @param plaintext- plaintext to be signed. type: bytes
    @return - signature of plaintext
"""


def signPlaintext(plaintext, keyPair):

    # Convert string plaintext to byte
    bplaintext = plaintext.encode()

    # get the hash valus of the plaintext
    hash = SHA256.new(bplaintext)

    # Sign the hash
    sig = PKCS115_SigScheme(keyPair)
    signature = sig.sign(hash)
    print("hex of signature: " + binascii.hexlify(signature))
    # this may need to be stored attahced to user object or in its database field - not sure
    return signature


# =============================================
# 4. The recieving end use this function to verify senders signature:
#   a) The plaintext passed to this function is the message recieved from the sender
#   b) The signature of the message needs to be passed to this function
#   c) The pubKey of the sender needs to be passed to this function
"""
    Verify message signature
    @param key - senders pubKey to use for verification
    @param plaintext- plaintext recieved message to be verified against pubKey. type: bytes
    @param signature- message signature which is paired with the message plaintext to be verified
    @return - True if match otherwise False for tampered message

"""


def verifySignature(plaintext, pubKey, signature):
    # get the hash from the message
    hash = SHA256.new(plaintext)
    # get the hash from the signature
    verifier = PKCS115_SigScheme.verify(pubKey)

    # compare
    try:
        verifier.verify(hash, signature)
        print("Signature is valid.")
        return True
    except:
        print("Signature is invalid.")
        return False
