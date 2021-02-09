# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2020
# Done by: Lin Huiqing (1003810)

import copy
from prettytable import PrettyTable

class Polynomial2:
    def __init__(self,coeffs):
        self.coeffs = coeffs

    def add(self,p2):
        return self._xor(p2)

    def sub(self,p2):
        return self._xor(p2)

    def _xor(self, p2):
        """ To calculate self XOR p2. 

            Returns:
                New Polynomial object of self XOR p2.
        """
        if len(self.coeffs) > len(p2.coeffs):
            poly_long, poly_short = self, p2
        else:
            poly_long, poly_short = p2, self 
        result = []
        for i, val_short in enumerate(poly_short.coeffs):
            if val_short == poly_long.coeffs[i]:
                result.append(0)
            else:
                result.append(1)
        result.extend(poly_long.coeffs[len(poly_short.coeffs):])
        return Polynomial2(result)

    def mul(self,p2,modp=None):
        result = Polynomial2([0])
        # iterates mulitplier to get product through long multiplier method
        for i, coeff in enumerate(p2.coeffs):
            if coeff == 1:
                result_shift = self._shift_right(i)
                result = result._xor(result_shift)
        # if modp is provided: result = result mod modp
        # self.div method is used to obtain remainder
        if modp != None:
            _, result = result.div(modp)
        return result

    def _shift_right(self, no_of_shifts):
        result = copy.copy(self)
        result.coeffs = [0]*no_of_shifts + result.coeffs
        return result

    def div(self,p2):
        # initialises variables
        numer = copy.copy(self)
        denom_len = len(p2.coeffs)
        q = []
        min_result = copy.copy(numer)
        stripped_zeroes = 0
        # perform long division
        # while numer can still divided, continue long division
        while len(numer.coeffs) >= denom_len:
            q = [1] + q
            numer_min = copy.copy(numer)
            numer_min.coeffs = numer_min.coeffs[-denom_len:]
            min_result = numer_min._xor(p2)
            stripped_zeroes = min_result._strip_zeroes()
            q = [0] * (stripped_zeroes-1) + q
            numer.coeffs = numer.coeffs[:-denom_len] + min_result.coeffs
            if min_result.coeffs == [0] * len(min_result.coeffs):
                q = min_result.coeffs + q
                break
        # if there should no trailing zeroes, remove zeroes
        if min_result.coeffs != [0] * len(min_result.coeffs):
            q = q[stripped_zeroes-1:]
        return Polynomial2(q), Polynomial2(numer.coeffs)

    def _strip_zeroes(self):
        zeroes = 0
        for i, val in enumerate(self.coeffs[::-1]):
            if val == 1:
                zeroes = i
                self.coeffs = self.coeffs[:-zeroes]
                break
        return zeroes

    def __str__(self):
        result = ""
        if self.coeffs == [0]:
            result = "0"
        for i, coeff in enumerate(self.coeffs):
            if coeff == 1:
                coeff_str = "x^{}+".format(i)
                result = coeff_str + result
        result = result.strip("+")
        return result

    def getInt(self):
        result = 0
        for i, val in enumerate(self.coeffs):
            if val == 1:
                result += 2**i
        return result


class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.x = x
        self.n = n
        self.ip = ip

    def add(self,g2):
        return self.getPolynomial2().add(g2.getPolynomial2())
    
    def sub(self,g2):
        return self.getPolynomial2().sub(g2.getPolynomial2())
    
    def mul(self,g2):
        return self.getPolynomial2().mul(g2.getPolynomial2(), self.ip)

    def div(self,g2):
        q, r = self.getPolynomial2().div(g2.getPolynomial2())
        q = GF2N(q.getInt())
        r = GF2N(r.getInt())
        return q, r

    def getPolynomial2(self):
        coeffs = "{0:b}".format(self.x)
        coeffs = [int(i) for i in coeffs]
        coeffs = coeffs[::-1]
        return Polynomial2(coeffs)

    def __str__(self):
        return str(self.getPolynomial2())

    def getInt(self):
        return self.x

    def mulInv(self):
        pass

    def affineMap(self):
        pass

# functions to create and display table (values are presented in integers)
def create_table(n, mode="*"):
    base_ls = []
    for i in range(2**n):
        base_ls.append(GF2N(i))
    table_rows = []
    row = []
    for row_base in base_ls:
        for col_base in base_ls:
            if mode == "*":
                row.append(row_base.mul(col_base))
            else:
                row.append(row_base.add(col_base))
        table_rows.append(row)
        row = []
    return base_ls, table_rows

def view_table(base_ls, table_rows, sign):
    base_ls = [str(base_val) for base_val in base_ls]
    header = [sign] + base_ls
    t = PrettyTable(header)
    for i, base_val in enumerate(base_ls):
        row = table_rows[i]
        row = [cell_val.getInt() for cell_val in row]
        t.add_row([base_val] + row)
    print(t)

print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3= p1+p2 =',p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=',p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=',p8q)
print('r for p6/p7=',p8r)

####
print('\nTest 4')
print('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 =',g1.getPolynomial2())
print('g2 =',g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 =',g3)

print('\nTest 5')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print('g4 =',g4.getPolynomial2())
print('g5 =',g5.getPolynomial2())
g6=g4.mul(g5)
print('g4 x g5 =',g6)

print('\nTest 6')
print('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print('g7 =',g7.getPolynomial2())
print('g8 =',g8.getPolynomial2())
q,r=g7.div(g8)
print('g7/g8 =')
print('q =',q.getPolynomial2())
print('r =',r.getPolynomial2())

# print('\nDiv Test')
# print('======')
# p6=Polynomial2([0,1])
# p7=Polynomial2([1])
# p8q,p8r=p6.div(p7)
# print(p8q)
# print(p8r)

# print('\nTest 7')
# print('======')
# ip=Polynomial2([1,1,0,0,1])
# print('irreducible polynomial',ip)
# g9=GF2N(0b101,4,ip)
# print('g9 =(',g9.getPolynomial2())
# print('inverse of g9 =',g9.mulInv().getPolynomial2())

# print('\nTest 8')
# print('======')
# ip=Polynomial2([1,1,0,1,1,0,0,0,1])
# print('irreducible polynomial',ip)
# g10=GF2N(0xc2,8,ip)
# print('g10 = 0xc2')
# g11=g10.mulInv()
# print('inverse of g10 = g11 =', hex(g11.getInt()))
# g12=g11.affineMap()
# print('affine map of g11 =',hex(g12.getInt()))

n = 4
sign = "*"
base_ls, table_rows = create_table(n, mode=sign)
view_table(base_ls, table_rows, sign)

sign = "+"
base_ls, table_rows = create_table(n, mode=sign)
view_table(base_ls, table_rows, sign)