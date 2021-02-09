import hashlib

LIST_OF_STRINGS = [b"THIS IS A STR", b"THIS IS ANOTHER STRING", b"egunb", b"nized", b"cance", b"opmen"]

if __name__ == "__main__":
    for test_str in LIST_OF_STRINGS:
        hashed_str = hashlib.md5(test_str)
        digest = hashed_str.hexdigest()
        print("plain str '{}' is of len {} while digest '{}' is of len {}".format(test_str, len(test_str), digest, len(digest)))