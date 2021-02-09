import base64
import random
import sys

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from primes import square_multiply


def extract_pub_key(pub_file):
    key = open(pub_file,"r")
    rsakey = RSA.importKey(key.read())
    n = rsakey.n
    e = rsakey.e
    return n, e

def extract_priv_key(priv_file):
    key = open(priv_file,"r")
    rsakey = RSA.importKey(key.read())
    n = rsakey.n
    d = rsakey.d
    return n, d

def read_file(filename):
    with open(filename) as f:
        return f.read()

def int_to_bytes(ip_int):
    return ip_int.to_bytes(length=(ip_int.bit_length() + 7) // 8, byteorder="little")

def encrypt_message(message, n, e):
    message_bytes = message.encode('utf-8')
    message_int = int.from_bytes(message_bytes, "little")
    return square_multiply(message_int, e, n)

def decrypt_cipher(cipher, n, d):
    message_int = square_multiply(cipher, d, n)
    message_bytes = int_to_bytes(message_int)
    return message_bytes.decode('utf-8')

def get_hash(message):
    h = SHA256.new()
    message_bytes = message.encode('utf-8')
    h.update(message_bytes)
    return h.hexdigest()

def get_signature(h_hex, n, d):
    h_int = int(h_hex, 16)
    return square_multiply(h_int, d, n)

def verify_signature(signature, n, e):
    message_int = square_multiply(signature, e, n)
    return hex(message_int).lstrip("0x")

if __name__ == "__main__":
    print("------------- Part I -------------")
    n, e = extract_pub_key("mykey.pem.pub")
    print("n: {}".format(n))
    print("e: {}".format(e))
    message = read_file("message.txt")
    print("message: {}".format(message))
    cipher = encrypt_message(message, n, e)
    print("encrypted message: {}".format(cipher))
    print()

    n, d = extract_priv_key("mykey.pem.priv")
    print("n: {}".format(n))
    print("d: {}".format(d))
    check_message = decrypt_cipher(cipher, n, d)
    print("decrypted message: {}".format(check_message))
    assert message == check_message
    print("message is the same as decrypted message!")
    print()

    message_hash = get_hash(message)
    print("message hash: {}".format(message_hash))
    signature = get_signature(message_hash, n, d)
    print("signature: {}".format(signature))
    print()

    check_hash = verify_signature(signature, n, e)
    print("retrieved hash: {}".format(check_hash))
    assert message_hash == check_hash
    print("message hash is the same as hash from signature!")
    print()

    print("------------- Part II -------------")
    print("------ RSA Encryption Protocol Attack ------")
    ip_int = 100
    print("Encrypting: {}".format(ip_int))
    print()

    ip_int_bytes = int_to_bytes(ip_int).decode('utf-8')
    y = encrypt_message(ip_int_bytes, n, e)
    print("Result: ")
    print(base64.b64encode(int_to_bytes(y)).decode("utf-8"))
    print()

    y_s = square_multiply(2, e, n)
    m = y * y_s % n
    print("Modified to: ")
    print(base64.b64encode(int_to_bytes(m)).decode("utf-8"))
    print()

    decrypted_int = square_multiply(m, d, n)
    print("Decrypted: {}".format(decrypted_int))
    print()
    
    print("------ RSA Digital Signature Attack ------")
    print("POV - Eve")
    random_signature = signature + random.randint(-sys.maxsize, sys.maxsize)
    print("random_signature: {}".format(random_signature))

    digest_x = verify_signature(random_signature, n, e)
    print("x: {}".format(digest_x))

    print("Sending s and x over to Alice...")
    print("POV - Alice")
    digest_x_prime = verify_signature(random_signature, n, e)
    print("x': {}".format(digest_x_prime))

    assert digest_x == digest_x_prime
    print("Since x = x', it is a valid signature!")

