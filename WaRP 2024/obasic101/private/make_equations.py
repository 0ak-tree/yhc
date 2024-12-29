import random
from pwn import p32

with open('../flag.txt', 'rb') as f:
    flag = f.read()

flag = [ i for i in flag ]

equation_matrix = [
    [ random.randrange(0, 256) for _ in range(len(flag)) ]
    for _ in range(len(flag))
]

result_vector = [ sum(equation_matrix[i][j] * flag[j] for j in range(len(flag))) for i in range(len(flag)) ]

print("Equations in C++ format:")
for i in range(len(flag)):
    print("if (", end="")
    for j in range(len(flag) - 1):
        print(f"{equation_matrix[i][j]} * input[{j}] + ", end="")
    
    result_vector_obfuscated = p32(result_vector[i])
    result_vector_obfuscated = "*(int*)xorstr_(\"\\x" + "\\x".join([ f"{i:02x}" for i in result_vector_obfuscated ]) + "\")"
    print(f"{equation_matrix[i][-1]} * input[{len(flag) - 1}] != {result_vector_obfuscated}) {{")
    print(f"    goto FAIL;")
    print("}")

print("Matrix:")
print(equation_matrix)

print("Result vector:")
print(result_vector)