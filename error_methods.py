def calculate_parity(data: bytes) -> str:
    sum_1 = 0

    for b in data:
        x=b
        while x > 1:
            if x & 1:
                sum_1 += 1
            x >>= 1
    parity_bit = sum_1 % 2
    return str(parity_bit)

def calculate_checksum(data: bytes, method: str) -> str:
    method = method.upper()

    if method == "PARITY":
        return calculate_parity(data)
    raise ValueError(f"Unsupported checksum method: {method}")