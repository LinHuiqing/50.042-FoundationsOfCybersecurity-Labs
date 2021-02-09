#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Done by: Lin Huiqing (1003810)
# Time: 107s

import hashlib
import json
import string
import time


def get_valid_char_set() -> list:
    """ To get valid character set (lowercase alphanumeric).

        Returns:
            List of valid character set to be used.
    """
    alphabet_string = string.ascii_lowercase
    char_list = list(alphabet_string)
    char_list.extend([str(no) for no in list(range(10))])
    return char_list

def hash_guess(message: str) -> str:
    """ To hash guess in MD5 and return the hex.

        Returns:
            String of hashed hex string.
    """
    hashed_str = hashlib.md5(message.encode())
    return hashed_str.hexdigest()

def get_possible_pw(char_set: list, hashed_pws: set, pw_len: int=5) -> dict:
    """ To get possible passwords of hashes. 

        Returns: 
            Dictionary which maps hashes to possible passwords.
    """
    hash_to_pw = {}
    input_indicies = [0] * pw_len
    max_pw = char_set[-1] * pw_len
    guess = ""
    while guess != max_pw and len(hashed_pws) != 0:
        guess = []
        for ip_idx in input_indicies:
            guess.append(char_set[ip_idx])
        guess = "".join(guess)
        hashed_guess = hash_guess(guess)

        for pos, ip_idx in enumerate(input_indicies):
            if ip_idx == len(char_set)-1:
                input_indicies[pos] = 0
            else:
                input_indicies[pos] += 1
                break

        if hashed_guess in hashed_pws:
            hashed_pws.remove(hashed_guess)
            print("collision: {} gives hash {}"\
                .format(guess, hashed_guess))
            hash_to_pw[hashed_guess] = guess
    return hash_to_pw

def get_hashed_pw(filename: str) -> list:
    """ To get hashed passwords from file.

        Returns: 
            List of hashed passwords.
    """
    with open(filename) as hash_file:
        lines = hash_file.read().splitlines()
    return lines

if __name__ == "__main__":
    start = time.time()
    char_set = get_valid_char_set()
    hashed_pws_ls = set(get_hashed_pw("hash5.txt"))
    print(hashed_pws_ls)
    hash_to_pw = get_possible_pw(char_set, hashed_pws_ls)
    print(hash_to_pw)
    end = time.time()
    t_time = end - start
    print("total time taken: {}".format(t_time))
    with open("hash5_1.json", "w") as output_file:
        json.dump(hash_to_pw, output_file)
