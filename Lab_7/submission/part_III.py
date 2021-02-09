from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS


def generate_RSA(filename, bits=1024):
    key = RSA.generate(bits)
    public_key = key.publickey()
    with open("{}.pem.pub".format(filename), "w") as pub_file:
        pub_file.write(public_key.exportKey("PEM").decode('utf-8'))
    with open("{}.pem.priv".format(filename), "w") as pub_file:
        pub_file.write(key.exportKey("PEM").decode('utf-8'))

def encrypt_RSA(public_key_file, message):
    key = RSA.importKey(open(public_key_file).read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message.encode('utf-8'))
    return ciphertext

def decrypt_RSA(private_key_file, ciphertext):
    key = RSA.importKey(open(private_key_file).read())
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(ciphertext)
    return message.decode('utf-8')

def sign_data(private_key_file, data):
    key = RSA.importKey(open(private_key_file).read())
    h = SHA.new()
    h.update(data.encode('utf-8'))
    signer = PKCS1_PSS.new(key)
    signature = signer.sign(h)
    return signature

def verify_sign(public_key_file, sign, data):
    data = data.encode('utf-8')
    key = RSA.importKey(open(public_key_file).read())
    h = SHA.new()
    h.update(data)
    verifier = PKCS1_PSS.new(key)
    if verifier.verify(h, sign):
        return True
    else:
        return False

if __name__ == "__main__":
    print("Generating RSA keys...")
    alice_key_name = "part_III_alice"
    bob_key_name = "part_III_bob"
    generate_RSA(alice_key_name)
    generate_RSA(bob_key_name)
    print("Keys for Alice and Bob have been generated.")
    print()

    print("POV - Alice")
    data = open("mydata.txt").read()
    ciphertext = encrypt_RSA("{}.pem.pub".format(bob_key_name), data)
    print("Encrypted data is: {}".format(ciphertext))

    signature = sign_data("{}.pem.priv".format(alice_key_name), data)
    print("Signature: {}".format(signature))
    print()

    print("POV - Bob")
    decrypted_data = decrypt_RSA("{}.pem.priv".format(bob_key_name), ciphertext)
    print("Decrypted data is: {}".format(decrypted_data))

    assert verify_sign("{}.pem.pub".format(alice_key_name), signature, decrypted_data)
    print("Signature has been verified!")
