#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# import libraries
import argparse
import subprocess

key_limit_lower, key_limit_higher = 0, 255
image_prefix = "part_III_images/img_"

def shift_cipher(filein,fileout,key):
    output = bytearray()
    with open(filein, mode="rb") as fin:
        text = fin.read()
    text_byte = bytearray(text)

    for byte in text_byte:
        output += bytearray([(byte+key)%(key_limit_higher+1)])
    
    with open(fileout, mode="wb") as fout:
        fout.write(output)

# our main function
if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein",help="input filename")

    # parse our arguments
    args = parser.parse_args()
    filein=args.filein

    for i in range(key_limit_lower, key_limit_higher+1):
        img_filename = "{}{}".format(image_prefix, i)
        shift_cipher(filein, img_filename, -i)
        process = subprocess.run(["file", img_filename], capture_output=True)
        file_des = process.stdout.decode("utf-8").split(":")[1].strip()
        if file_des.startswith("PNG"):
            print("{} is a PNG file!".format(img_filename))
