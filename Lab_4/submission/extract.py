#!/usr/bin/env python3
# ECB plaintext extraction file for 50.042 FCS
# Done by: Lin Huiqing (1003810)

import argparse

def get_file_content(filename, mode):
    with open(filename, mode) as in_file:
        bits = in_file.read()
    return bits
    
def write_content_to_file(content, filename, mode):
    with open(filename, mode) as out_file:
        out_file.write(content)

def getInfo(headerfile):
    return get_file_content(headerfile, "rb")

def extract(infile,outfile,headerfile):
    header = getInfo(headerfile)
    file_start = len(header)+1
    file_content = get_file_content(infile, "rb")[file_start:]
    block_size = 8
    first_block = file_content[:block_size]
    assert len(file_content) % block_size == 0
    cycles = len(file_content) // block_size
    output = header + bytes(block_size*30)
    for i in range(cycles):
        block = file_content[i*block_size:(i+1)*block_size]
        if block == first_block:
            output += bytes(block_size)
        else:
            output += b'11111111'
    write_content_to_file(output, outfile, "wb")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)

    extract(infile,outfile,headerfile)
