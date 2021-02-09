import subprocess
import os

def rainbow_table_lookup(plaintext_len, filename):
    plaintext_len = str(plaintext_len)
    # output = ""
    print("""
    ----------------------------
    cracking {}
    ----------------------------
    """.format(filename))
    # subprocess.run(["cd", "rainbowcrack"])
    # os.chdir("./rainbowcrack/")
    # subprocess.call(["./rainbowcrack/rtgen", "md5", "loweralpha-numeric", plaintext_len, plaintext_len, "0", "3800", "600000", "0"])
    # subprocess.call(["./rainbowcrack/rtsort", "./rainbowcrack"])
    # popen = subprocess.Popen(["./rainbowcrack/rcrack", "./rainbowcrack", "md5_loweralpha-numeric#{}-{}_0_3800x600000_0.rt".format(plaintext_len, plaintext_len), "-l", filename], stdout=subprocess.PIPE)
    # for stdout_line in iter(popen.stdout.readline, ""):
    #     yield stdout_line 
    # popen.stdout.close()
    process = subprocess.run(["./rcrack", ".", "md5_loweralpha-numeric#{}-{}_0_3800x600000_0.rt".format(plaintext_len, plaintext_len), "-l", filename], capture_output=True)
    print(process.stdout.decode("utf-8"))
    # output, _ = p.communicate()
    # print(output)

if __name__ == "__main__":
    print(os.getcwd())
    rainbow_table_lookup(5, "hash5.txt")
    rainbow_table_lookup(6, "salted6.txt")