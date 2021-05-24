from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
# 1. need to import the appropriate class to supply the user's  keypair

# ======================================================
# 2. keyPair needs to be passed to this function for signing -
# what is the format of the keyPair and which function passes it?
# some options are: store in the database, .pem file
# 3. the function converts plaintext to bytes
"""
    Generates DSA key
    @param client - is passed so the function so that it can be added as 
        a prefix to the generated DSA_public_key.pem 
    @return - DSA key
"""


def genDSA_keys(client):
    # Create a new DSA key
    key = DSA.generate(2048)
    f = open(client+"DSA_public_key.pem", "wb")
    f.write(key.publickey().export_key())
    f.close()


"""
    Sign plaintext with DSA key
    @param key - the key to use
    @param plaintext- plaintext to be signed. type: bytes
    @return - signature of plaintext
"""


def DSA_sign(key, message):
    # Sign a message
    message = b"Hello"
    hash_obj = SHA256.new(message)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(hash_obj)
    # signature = hex(signature)
    return signature


"""
    Verify message signature
    @param key - senders pubKey to use for verification
    @param plaintext- plaintext recieved message to be verified against pubKey. type: bytes
    @param signature- message signature which is paired with the message plaintext to be verified
    @return - True if match otherwise False for tampered message

"""


def DSA_verifier(pub_key, message, signature, client):
    # Load the public key
    f = open(client+"DSA_public_key.pem", "rb")
    hash_obj = SHA256.new(message)
    pub_key = DSA.import_key(f.read())
    verifier = DSS.new(pub_key, 'fips-186-3')

    # Verify the authenticity of the message
    try:
        verifier.verify(hash_obj, signature)
        print("The message is authentic.")
    except ValueError:
        print("The message is not authentic.")
