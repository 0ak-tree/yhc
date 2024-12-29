with open('이세계로 전생했더니 순정 모험 라이프.pdf.yorixpub', 'rb') as f:
    response = f.read()

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open('leaked_private.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

def decrypt(ciphertext):
    decrypted = private_key.decrypt(
        ciphertext,
        padding.PKCS1v15()
    )
    return decrypted

from pwn import *
from Crypto.Util.number import bytes_to_long

assert response[:4] == b"YPUB"

ptr = 4

keyname_len = u64(response[ptr:ptr+8])
ptr += 8

keyname = response[ptr:ptr+keyname_len]
ptr += keyname_len

e_len = u64(response[ptr:ptr+8])
ptr += 8

e = bytes_to_long(response[ptr:ptr+e_len])
ptr += e_len

n_len = u64(response[ptr:ptr+8])
ptr += 8

n = bytes_to_long(response[ptr:ptr+n_len])
ptr += n_len

rsa_aes_key_len = u64(response[ptr:ptr+8])
ptr += 8

rsa_aes_key = decrypt(response[ptr:ptr+rsa_aes_key_len])
ptr += rsa_aes_key_len

from Crypto.Cipher import AES

cipher_len = u64(response[ptr:ptr+8])
ptr += 8

cipher = response[ptr:ptr+cipher_len]
ptr += cipher_len

assert len(rsa_aes_key) == 32

aes = AES.new(rsa_aes_key, AES.MODE_ECB)

Eb = aes.decrypt(cipher)
IV = list(Eb[:16])

for i, (a, b) in enumerate(zip(IV, b"YORIX_MAGIC_HEAD")):
    IV[i] = a ^ b

aes_cbc = AES.new(rsa_aes_key, AES.MODE_CBC, bytes(IV))

file_data = aes_cbc.decrypt(cipher)[18:]

with open('decrypted.pdf', 'wb') as f:
    f.write(file_data)

print("pwned")