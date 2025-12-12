from error_methods import calculate_checksum

if __name__ == "__main__":
    metin = input("Metni gir: ")
    data_bytes = metin.encode("utf-8")

    method = "PARITY"
    kontrol = calculate_checksum(data_bytes, method)

    print(f"Data: {metin}")
    print(f"Method: {method}")
    print(f"Parity bit: {kontrol}")