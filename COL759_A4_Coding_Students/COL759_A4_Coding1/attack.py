# from mrsa import dec, restart_system
# import math

# def attack():
#     """
#     Function details:
#     restart_system(): It will return ((N, e), ct) where (N, e) is the public key and ct is the ciphertext you have to decrypt
#         - You can call it maximum of 200 times
#     dec(ct, N, d): It will return message corresponding to the given ciphertext ct using N and d
#     """
   

#     """
#     return the message corresponding to the ciphertext you got from restart_sytem
#     """
#     return None

from mrsa import dec, restart_system

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def pollards_rho(n):
    x = 2
    y = 2
    d = 1
    f = lambda x: (x**2 + 1) % n

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)

    if d == n:
        return None  # Factorization failed
    return d

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0

    return x1 + m0 if x1 < 0 else x1

def calculate_private_key(e, p, q):
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    return d

def attack():
    attempts = 0

    while attempts < 200:
        # Restart the system to obtain public key and ciphertext
        ((N, e), ct) = restart_system()

        # Factorize N to obtain prime factors
        p = pollards_rho(N)
        if p is not None:
            q = N // p

            # Calculate private key
            d = calculate_private_key(e, p, q)

            # Decrypt the ciphertext
            message = dec(ct, N, d)

            return message

        attempts += 1

    # If no successful attack after 200 attempts, return None
    return None
