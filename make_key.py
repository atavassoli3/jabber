from Crypto.PublicKey import RSA

def make_keys(userName):
    # Generate a public/private key pair
    private_key = RSA.generate(1024)

    # Get the private key
    public_key = private_key.publickey()

    # The private key bytes to print
    privKeyBytes = private_key.exportKey(format='PEM')

    # The public key bytes to print
    pubKeyBytes = public_key.exportKey(format='PEM')

    # Save the private key
    with open (userName+"-private.pem", "wb") as prv_file:
        prv_file.write(privKeyBytes)

    # Save the public key
    with open (userName+"-public.pem", "wb") as pub_file:
        pub_file.write(pubKeyBytes)

make_keys(input("Enter username: "))