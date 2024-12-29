from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open('keys/private.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

#print(hex(private_key.public_key().public_numbers().n))
print(hex(private_key.private_numbers().d))