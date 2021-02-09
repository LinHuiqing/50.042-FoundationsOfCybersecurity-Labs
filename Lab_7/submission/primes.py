# 50.042 FCS Lab 6 template
# Year 2020
# Done by: Lin Huiqing (1003810)

import random
def square_multiply(a,x,n):
    y = 1
    x_bin = "{0:b}".format(x)
    for x_i in x_bin:
        y = (y**2) % n
        if x_i == "1":
            y = (a*y) % n
    y = y % n
    return y

def miller_rabin(n, a):
    pass

def gen_prime_nbits(n):
    pass

if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561,2))
    print('Is 27 a prime?')
    print(miller_rabin(27,2))
    print('Is 61 a prime?')
    print(miller_rabin(61,2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))

    print(square_multiply(5,40,7))
