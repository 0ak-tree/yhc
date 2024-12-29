with open("flag.txt", "rb") as f:
    flag = f.read()
flag_len = len(flag)

redacted = b"[REDACTED]"
redacted_padded = b"[REDACTED]" * (flag_len // len(redacted)) + redacted[: flag_len % len(redacted)]

print("0x" + redacted_padded.hex())