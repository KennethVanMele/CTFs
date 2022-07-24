# CTFs
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

# application of Extended Euclidean Algorithm to find a modular inverse
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    return int(x % m) 
    
P = 61
N = 3233
Q = N/P
T=(P-1)*(Q-1)
E=17
D=modinv(E, T)
C=2790
M=pow(C,D,N)
print(M)
