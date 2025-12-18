from __future__ import annotations
from typing import Iterable

def _format_hex(value: int, width_nibbles: int) -> str:
    return f"{value:0{width_nibbles}X}"

def _bytes_to_bits(data: bytes) -> list[int]:
    bits: list[int] = []
    for b in data:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    return bits

def calculate_checksum(data: bytes, method: str) -> str:
    m = method.strip().upper()

    if m in {"PARITY", "PARITY_EVEN", "EVEN_PARITY", "EVEN"}:
        return _parity_even_bit(data)

    if m in {"PARITY_ODD", "ODD_PARITY", "ODD"}:
        return _parity_odd_bit(data)

    if m in {"2D_PARITY", "2DPARITY", "MATRIX_PARITY"}:
        return _parity_2d(data)

    if m in {"CRC16", "CRC-16"}:
        return _crc16(data)

    if m in {"CRC32", "CRC-32"}:
        return _crc32(data)

    if m in {"INTERNET_CHECKSUM", "IP_CHECKSUM", "CHECKSUM"}:
        return _internet_checksum(data)

    raise ValueError(f"Unsupported checksum method: {method}")

def _parity_even_bit(data: bytes) -> str:
    ones = sum(_bytes_to_bits(data))
    return str(ones % 2)

def _parity_odd_bit(data: bytes) -> str:
    return "0" if _parity_even_bit(data) == "1" else "1"

def _parity_even_of_bits(bits: Iterable[int]) -> int:
    ones = sum(bits)
    return 0 if ones % 2 == 0 else 1

def _parity_2d(data: bytes) -> str:
    rows = []
    for b in data:
        rows.append([(b >> i) & 1 for i in range(7, -1, -1)])

    if not rows:
        return ":" + "0" * 8

    row_parity = "".join(str(_parity_even_of_bits(r)) for r in rows)

    col = []
    for c in range(8):
        col.append(_parity_even_of_bits(row[c] for row in rows))
    col_parity = "".join(str(x) for x in col)

    return f"{row_parity}:{col_parity}"

def _reflect_bits(x: int, width: int) -> int:
    r = 0
    for i in range(width):
        r = (r << 1) | ((x >> i) & 1)
    return r

def _crc_generic(data: bytes, width: int, poly: int, init: int, xorout: int, refin: bool, refout: bool) -> int:
    mask = (1 << width) - 1
    topbit = 1 << (width - 1)
    crc = init & mask

    for b in data:
        cur = _reflect_bits(b, 8) if refin else b
        crc ^= (cur << (width - 8)) & mask
        for _ in range(8):
            if crc & topbit:
                crc = ((crc << 1) ^ poly) & mask
            else:
                crc = (crc << 1) & mask

    if refout:
        crc = _reflect_bits(crc, width) & mask

    return (crc ^ xorout) & mask

def _crc16(data: bytes) -> str:
    v = _crc_generic(data, 16, 0x1021, 0xFFFF, 0x0000, refin=False, refout=False)
    return _format_hex(v, 4)

def _crc32(data: bytes) -> str:
    v = _crc_generic(data, 32, 0x04C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, refin=True, refout=True)
    return _format_hex(v, 8)

def _internet_checksum(data: bytes) -> str:
    if len(data) % 2 == 1:
        data += b"\x00"

    s = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        s += word
        s = (s & 0xFFFF) + (s >> 16)

    checksum = (~s) & 0xFFFF
    return _format_hex(checksum, 4)

