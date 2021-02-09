#!/usr/bin/python3
# -*- coding: utf-8 -*-
# DA+Nils 2018
# Andrei + Z.TANG + Bowen + Saket, 2020
# Done by: Lin Huiqing (1003810)

"""
Lab2: Breaking Ciphers

Pwntool client for python3

Install: see install.sh

Documentation: https://python3-pwntools.readthedocs.io/en/latest/
"""

from pwn import remote


ENG_LETTER_FREQ = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

# helper functions for sol1
def collate_freq(encrypted_str:str) -> dict:
    """ To count the frequency of letters in the encrypted string.

        Args: 
            encrypted_str - string which has been encrypted.

        Returns:
            Dictionary containing all letters and their respective frequencies.
    """
    letter_dict = {}
    total_char = 0
    for char in encrypted_str:
        if char.isalpha():
            total_char += 1
            letter_dict[char] = letter_dict.get(char, 0) + 1
    return letter_dict

def order_char_on_freq(char_freq_dict: dict):
    """ To order characters in a dictionary based on their frequencies.

        Args:
            char_freq_dict - given dictionary of characters.

        Returns: 
            List of characters in order of frequency.
    """
    letter_ls = []
    for char, count in char_freq_dict.items():
        letter_ls.append((char, count))
    letter_ls.sort(key=lambda tup: tup[1], reverse=True)
    return letter_ls

def likely_mapping(eng_order, challenge_order):
    """ To create a likely mapping of letters based on frequency analysis.

        Args: 
            eng_order - list of letters in order of frequency in the english language.
            challenge_order - list of letters in order of frequency in the given encrypted string.
        
        Returns:
            Dictionary containing likely mapping of characters.
    """
    mapping_dict = {}
    for idx, tup in enumerate(challenge_order):
        mapping_dict[tup[0]] = eng_order[idx][0]
    return mapping_dict

def decode_challenge(mapping_dict, encrypted_str):
    """ To decode encrypted string given a mapping of letters.

        Args:
            mapping_dict - dictionary to map letters to decrypt.
            encrypted_str - given encrypted string.

        Returns:
            Decrypted string.
    """
    encrypted_ls = list(encrypted_str)
    for idx, letter in enumerate(encrypted_ls):
        encrypted_ls[idx] = mapping_dict.get(letter, letter)
    return "".join(encrypted_ls)

# helper function for sol2
# pass two bytestrings to this function
def XOR(a, b):
    """ To XOR 2 bytes inputs.

        Args:
            a - first set of bytes.
            b - second set of bytes.

        Returns:
            Bytes representing a XOR b.
    """
    r = b''
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r


def sol1():
    conn.send("1")  # select challenge 1
    challenge = conn.recv()
    print("Question 1:\n")
    # decrypt the challenge here
    challenge = challenge.decode()
    letter_freq_dict = collate_freq(challenge)
    challenge_list = order_char_on_freq(letter_freq_dict)
    eng_list = order_char_on_freq(ENG_LETTER_FREQ)
    first_map = likely_mapping(eng_list, challenge_list)
    
    first_map["P"] = "H"
    first_map["F"] = "Y"
    first_map["I"] = "O"
    first_map["O"] = "G"
    first_map["U"] = "W"
    first_map["W"] = "C"
    first_map["G"] = "U"
    first_map["Y"] = "B"
    first_map["T"] = "M"
    first_map["J"] = "P"
    first_map["K"] = "Q"
    first_map["B"] = "Z"
    first_map["L"] = "S"
    first_map["Z"] = "N"
    first_map["N"] = "F"
    first_map["X"] = "V"
    first_map["V"] = "X"

    solution = decode_challenge(first_map, challenge)
    print("Part I answer: {}\n".format(solution))
    conn.send(solution)
    message = conn.recv()
    print("Part I response:")
    if b'Congratulations' in message:
        print(message.decode())


def sol2():
    conn.send("2")  # select challenge 2
    challenge = conn.recv()
    print("\nQuestion 2:\n")
    challenge = challenge.decode("UTF-8")
    challenge = bytes.fromhex(challenge)

    mask = bytes(14) + bytes([3, 8, 1, 0]) + bytes(6) + bytes([4]) + bytes(7)
    message = XOR(challenge, mask)
    print("Part II answer: {}\n".format(message))
    conn.send(message)
    message = conn.recv()
    print("Part II response:")
    if b'points' in message:
        print(message)

if __name__ == "__main__":
    URL = "35.198.199.82"
    PORT = 4455

    conn = remote(URL, PORT)
    receive1 = conn.recv()
    print(receive1.decode("UTF-8"))

    sol1()
    sol2()
    conn.close()
