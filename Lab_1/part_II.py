#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Code for Part II


# import libraries
import argparse

# set up constants for code
key_limit_lower, key_limit_higher = 0, 255

# function to encrypt and decrypt method 
def shift_cipher(filein: str,fileout: str,key: int) -> None:
    """ To shift characters in the alphabet according to key. 
    
        Args:
            filein - input file name
            fileout - output file name
            key - no. of characters to shift by
    """
    # read file and convert to bytearray
    with open(filein, mode="rb") as fin:
        text = fin.read()
    text_byte = bytearray(text)

    # shift each byte by key value and add to output
    output = bytearray()
    for byte in text_byte:
        output += bytearray([(byte+key)%(key_limit_higher+1)])
    
    # write output to file
    with open(fileout, mode="wb") as fout:
        fout.write(output)

# our main function
if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein",help="input filename")
    parser.add_argument("-o", dest="fileout", help="output filename")
    parser.add_argument("-k", dest="key", help="key (int between {} and {})" \
        .format(key_limit_lower, key_limit_higher))
    parser.add_argument("-m", dest="mode", help="mode ('e' or 'd')")

    # parse our arguments
    args = parser.parse_args()
    filein=args.filein
    fileout=args.fileout
    key=args.key
    mode=args.mode

    # check that key input is a valid integer
    try:
        key=int(key)
    except:
        raise ValueError("please input a valid integer for -k")

    if not (key_limit_lower <= key <= key_limit_higher):
        raise ValueError("please input an integer between {} and {} for -k" \
            .format(key_limit_lower, key_limit_higher))

    # shift characters according to mode
    if mode.lower() == "e":
        shift_cipher(filein,fileout,key)
    elif mode.lower() == "d":
        shift_cipher(filein,fileout,-key)
    else:
        raise ValueError("-m input can only be 'e' or 'd'")
