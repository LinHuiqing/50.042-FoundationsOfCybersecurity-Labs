#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Done by: Lin Huiqing (1003810)
# Time to crack plain passwords: 6.49s
# Time to crack salted passwords: 58.97s

import hashlib
import json
import random
import string


def get_valid_char_set() -> list:
    """ To get valid character set (lowercase alphanumeric).

        Returns:
            List of valid character set to be used.
    """
    return list(string.ascii_lowercase)

def get_passwords(filename: str) -> list:
    """ To get passwords from file.

        Returns: 
            List of passwords.
    """
    with open(filename) as input_file:
        hash_to_pw = json.load(input_file)
    return list(hash_to_pw.values())

def salt_pw(password: str, char_set: list) -> str:
    """ To add a random salt to password.

        Returns:
            String of salted password.
    """
    salt = random.choice(char_set)
    return password + salt

def hash_message(message: str) -> str:
    """ To hash input string (password).

        Returns:
            String of hash of salted password.
    """
    hashed_str = hashlib.md5(message.encode())
    return hashed_str.hexdigest()

def get_salted_and_hash(password_ls: list, char_set: list) -> dict:
    """ To get salted passwords and their hashes.

        Returns:
            Dictionary which maps salted password hashes to their respective 
            salted passwords.
    """
    hash_to_pw = {}
    for pw in password_ls:
        salted_pw = salt_pw(pw, char_set)
        hashed_salted_pw = hash_message(salted_pw)
        hash_to_pw[salted_pw] = hashed_salted_pw
    return hash_to_pw

def write_to_txt(input_ls: list, filename: str) -> None:
    """ To write list of strings to txt file. """
    file_str = "\n".join(input_ls)
    with open(filename, 'w') as input_file:
        input_file.write(file_str)

if __name__ == "__main__":
    char_set = get_valid_char_set()
    passwords = get_passwords("hash5.json")
    hash_to_pw = get_salted_and_hash(passwords, char_set)
    write_to_txt(list(hash_to_pw.values()), "salted6.txt")
    write_to_txt(list(hash_to_pw.keys()), "pass6.txt")
