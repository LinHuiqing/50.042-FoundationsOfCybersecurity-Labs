#!/usr/bin/env python3
# ECB wrapper file for 50.042 FCS
# Done by: Lin Huiqing (1003810)

import argparse
import secrets

from present import *

nokeybits=80
blocksize=64

def generate_key(key_length):
    return secrets.token_bytes(key_length)

def get_file_content(filename, mode):
    with open(filename, mode) as in_file:
        bits = in_file.read()
    return bits

def write_content_to_file(content, filename, mode):
    with open(filename, mode) as out_file:
        out_file.write(content)

def ecb(infile,outfile,key,mode):
    print("executing ecb {} mode...".format(mode))
    content = get_file_content(infile, "rb")
    byte_blocksize = blocksize // 8
    
    remainder = len(content) % byte_blocksize
    if remainder != 0:
        content = content + bytes(byte_blocksize-remainder)
    cycles = len(content) // byte_blocksize
    output = bytes(0)
    for i in range(cycles):
        block = content[i*byte_blocksize:(i+1)*byte_blocksize]
        block = int.from_bytes(block, "big")
        if mode == "encrypt":
            cipher = present(block, key)
        elif mode == "decrypt":
            cipher = present_inv(block, key)
        output += (cipher).to_bytes(byte_blocksize, "big")
    write_content_to_file(output, outfile, "wb")

if __name__=="__main__":
    # uncomment to generate key and save it in keyfile
    # key = generate_key(nokeybits)
    # write_content_to_file(key, "keyfile", "wb")

    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile
    mode=args.mode

    key = get_file_content(keyfile, "rb")
    key = int.from_bytes(key, "big")
    ecb(infile,outfile,key,mode)
