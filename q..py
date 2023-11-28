import random
import math
from mrsa import restart_system, dec

def attack():
    # Constants
    max_attempts = 200

    # Initialize variables
    collected_keys = []

    for _ in range(max_attempts):
        # Restart the system to get a new public key and ciphertext
        (N, e), ct = restart_system()

        # Store the collected public keys
        collected_keys.append((N, e))

        # Check if we have enough samples to attempt factorization
        if len(collected_keys) >= 3:
            # Attempt to factorize N using collected public keys
            factors = try_factorization(collected_keys)

            # If factorization succeeds, break out of the loop
            if factors:
                break

    # Calculate private key using the factorized N
    d = calculate_private_key(factors, e)

    # Decrypt the latest ciphertext using the obtained private key
    message = dec(ct, N, d)

    return message

def try_factorization(keys):
    # Try factorizing the latest modulus using Pollard's Rho algorithm with cycle detection
    latest_N = keys[-1][0]
    factors = pollards_rho_factorization(latest_N)

    # Check if factorization succeeded
    if factors:
        return factors
    else:
        return None

def pollards_rho_factorization(N):
    # Pollard's Rho algorithm with cycle detection
    x = random.randint(1, N - 1)
    y = x
    d = 1
    count = 0  # Counter to limit the number of iterations

    f = lambda x: (x**2 + 1) % N

    while d == 1 and count < 2 * int(math.sqrt(N)):  # Limit the number of iterations
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), N)
        count += 1

    if d != N:
        return (d, N // d)
    else:
        # Return None if Pollard's rho does not find a factor
        return None

def calculate_private_key(factors, e):
    # Calculate the private key using the factorized N and public exponent e
    p, q = factors
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return d