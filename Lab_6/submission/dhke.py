# 50.042 FCS Lab 6
# Year 2020
# Done by: Lin Huiqing (1003810)

import primes 
import random
import ecb
import argparse
import wolframalpha

def dhke_setup(nb):
    # gets prime number through wolframalpha's API
    client = wolframalpha.Client("29EWXE-3A4434672Q") # app-id for wolframalpha API
    res = client.query('prime closest to 2^{}'.format(nb))
    p = int(res["pod"][1]["subpod"]["plaintext"])
    alpha = random.randint(2, p-2)
    return p, alpha

def gen_priv_key(p):
    return random.randint(2, p-2)

def get_pub_key(alpha, a, p):
    return primes.square_multiply(alpha,a,p)

def get_shared_key(keypub,keypriv,p):
    return primes.square_multiply(keypub, keypriv, p)
    
if __name__=="__main__":
    p,alpha= dhke_setup(128)
    print('Generate P and alpha:')
    print('P:',p)
    print('alpha:',alpha)
    print()
    a=gen_priv_key(p)
    b=gen_priv_key(p)
    print('My private key is: ',a)
    print('Test other private key is: ',b)
    print()
    A=get_pub_key(alpha,a,p)
    B=get_pub_key(alpha,b,p)
    print('My public key is: ',A)
    print('Test other public key is: ',B)
    print()
    sharedKeyA=get_shared_key(B,a,p)
    sharedKeyB=get_shared_key(A,b,p)
    print('My shared key is: ',sharedKeyA)
    print('Test other shared key is: ',sharedKeyB)
    print('Length of key is %d bits.'%sharedKeyA.bit_length())

    assert (sharedKeyA==sharedKeyB)
    print("Shared key for both users is the same!")

    parser=argparse.ArgumentParser(description='Transfer of files with keys shared through Diffie-Hellman Key Exchange and encryption protocol block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file', default='transfer_file.jpg')
    parser.add_argument('-o', dest='outfile',help='output file', default='encrypted_file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile

    print("encrypting file...")
    ecb.ecb(infile,outfile,sharedKeyA,"encrypt")
    print("decrypting file...")
    ecb.ecb(outfile,"original.jpg",sharedKeyA,"decrypt")