g = [34594090194318967965199850975854278818752424473343042725311968237869666519515,53834109148761994916864666554335027158413503244549450445486447921913414271610,31209359426067756217053611950622267858441051633228366697484629172980136848477]
N = 0x904a62a90a9403429ad10d4336295fa07230bdf037ba216e803dd0acf0458acd
from Crypto.Util.number import long_to_bytes, bytes_to_long
from web3 import Web3

k = bytes_to_long(Web3.keccak(b"yorix' amazing key lmao"))
k_inv = pow(k, -1, N)

flag = b""
for i in range(len(g)):
    flag += long_to_bytes((g[i] * k_inv) % N)

print(flag)
