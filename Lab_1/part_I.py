#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Code for Part I


# import libraries
import argparse
import string

# set up constants for code
valid_alphabet = list(string.printable)
key_limit_lower, key_limit_higher = 1, len(valid_alphabet)-1

# function to encrypt and decrypt method 
def shift_cipher(filein: str,fileout: str,key: int) -> None:
    """ To shift characters in the alphabet according to key. 
    
        Args:
            filein - input file name
            fileout - output file name
            key - no. of characters to shift by
    """
    # read, shift and save characters
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        output = []
        for char in text:
            org_idx = valid_alphabet.index(char)
            new_idx = (org_idx + key) % len(valid_alphabet)
            output.append(valid_alphabet[new_idx])
    
    # write new characters to file
    with open(fileout, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write("".join(output))

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
