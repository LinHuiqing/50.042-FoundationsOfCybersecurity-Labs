# 50.042 FCS Lab 6
# Year 2020
# Done by: Lin Huiqing (1003810)

import math
import primes
import dhke
import time

def calc_m(G):
    return math.floor(math.sqrt(abs(G)))

def baby_step(alpha,beta,p,fname):
    m = calc_m(p)
    inter_ls = []
    for xb in range(m):
        inter = (primes.square_multiply(alpha, xb, p) * beta) % p
        inter_ls.append(str(inter))
    with open(fname, "w") as outfile:
        output = "\n".join(inter_ls)
        outfile.write(output)
    return inter_ls
    
def giant_step(alpha,p,fname):
    m = calc_m(p)
    inter_ls = []
    for xg in range(m):
        inter = primes.square_multiply(alpha, (m*xg), p)
        inter_ls.append(str(inter))
    with open(fname, "w") as outfile:
        output = "\n".join(inter_ls)
        outfile.write(output)
    return inter_ls

def baby_giant(alpha,beta,p):
    baby_step_fname = "baby_step_inter.txt"
    giant_step_fname = "giant_step_inter.txt"
    baby_step_values = baby_step(alpha, beta, p, baby_step_fname)
    giant_step_values = giant_step(alpha, p, giant_step_fname)

    m = calc_m(p)

    for baby_idx, baby_step_row in enumerate(baby_step_values):
        baby_step_v = baby_step_row.split(";")
        for giant_idx, giant_step_row in enumerate(giant_step_values):
            giant_step_v = giant_step_row.split(";")
            if baby_step_v == giant_step_v:
                x = giant_idx * m - baby_idx
                return x
    
    # Raise error when no match is found
    raise ValueError("No match found.")

if __name__=="__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    
    """
    p=17851
    alpha=17511
    A=2945
    B=11844
    sharedkey=1671
    a=baby_giant(alpha,A,p)
    b=baby_giant(alpha,B,p)
    guesskey1=primes.square_multiply(A,b,p)
    guesskey2=primes.square_multiply(B,a,p)
    print('Guess key 1:',guesskey1)
    print('Guess key 2:',guesskey2)
    print('Actual shared key :',sharedkey)

    for i in range(3):
        # generates 16-bit shared keys and breaks them, taking note of the time
        print("trial {}".format(i+1))
        p, alpha = dhke.dhke_setup(16)
        a = dhke.gen_priv_key(p)
        b = dhke.gen_priv_key(p)
        A = dhke.get_pub_key(alpha,a,p)
        B = dhke.get_pub_key(alpha,b,p)
        sharedkey = dhke.get_shared_key(B,a,p)

        start = time.time()
        a=baby_giant(alpha,A,p)
        b=baby_giant(alpha,B,p)
        guesskey1=primes.square_multiply(A,b,p)
        guesskey2=primes.square_multiply(B,a,p)
        print('Guess key 1:',guesskey1)
        print('Guess key 2:',guesskey2)
        print('Actual shared key :',sharedkey)
        end = time.time()
        t_time = end - start
        print("total time taken: {}".format(t_time))
