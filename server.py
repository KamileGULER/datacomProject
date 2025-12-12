import socket
import random
import string

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 5000

RECEIVER_HOST = "127.0.0.1"
RECEIVER_PORT = 6000


def char_substitution(data: str) -> str:
    if not data:
        return data
    index = random.randrange(len(data))
    original_char = data[index]
    candidates = string.ascii_letters + string.digits + string.punctuation + " "
    candidates = candidates.replace(original_char, "") or candidates
    new_char = random.choice(candidates)
    return data[:index] + new_char + data[index + 1:]


def char_deletion(data: str) -> str:
    if len(data) <= 1:
        return data
    index = random.randrange(len(data))
    return data[:index] + data[index + 1:]


def char_insertion(data: str) -> str:
    index = random.randrange(len(data) + 1)
    new_char = random.choice(string.ascii_letters + string.digits + string.punctuation + " ")
    return data[:index] + new_char + data[index:]


def char_swapping(data: str) -> str:
    if len(data) < 2:
        return data
    index = random.randrange(len(data) - 1)
    lst = list(data)
    lst[index], lst[index + 1] = lst[index + 1], lst[index]
    return "".join(lst)


def flip_random_bit_in_char(data: str) -> str:
    if not data:
        return data
    index = random.randrange(len(data))
    ch = data[index]

    code_point = ord(ch)
    bit_pos = random.randint(0, 7)
    flipped = code_point ^ (1 << bit_pos)
    new_char = chr(flipped)
    return data[:index] + new_char + data[index + 1:]


def multiple_bit_flips(data: str, count: int = 3) -> str:
    result = data
    for _ in range(count):
        result = flip_random_bit_in_char(result)
    return result


def burst_error(data: str, length: int = 3) -> str:
    if len(data) < 1:
        return data

    length = min(length, len(data))

    start = random.randrange(len(data) - length + 1)
    end = start + length

    burst = "".join(random.choice(string.printable) for _ in range(length))

    return data[:start] + burst + data[end:]


def corrupt_data_randomly(data: str, debug: bool = True) -> tuple[str, str]:
    """
    Corrupt data randomly using one of the error injection methods.
    
    Args:
        data: The data string to corrupt
        debug: Whether to print debug messages (default: True)
        
    Returns:
        tuple: (corrupted_data, error_method_name)
        - corrupted_data: The corrupted string (or original if no error)
        - error_method_name: Name of the method used, or "none" if no error
    """
    if not data:
        return data, "none"

    # 50% chance: no error
    if random.random() < 0.5:
        if debug:
            print("[DEBUG] No error applied.")
        return data, "none"

    methods = [
        ("char_substitution", char_substitution),
        ("char_deletion", char_deletion),
        ("char_insertion", char_insertion),
        ("char_swapping", char_swapping),
        ("bit_flip", flip_random_bit_in_char),
        ("multiple_bit_flips", lambda d: multiple_bit_flips(d, count=3)),
        ("burst_error", lambda d: burst_error(d, length=3)),
    ]

    method_name, chosen_method = random.choice(methods)
    if debug:
        print(f"[DEBUG] Error method used: {method_name}")
    
    corrupted = chosen_method(data)
    return corrupted, method_name


def process_packet(packet_str: str, debug: bool = True) -> tuple[str, str, str, str, bool, str]:
    """
    Process a packet: parse it, corrupt the data, and create a new packet.
    
    Args:
        packet_str: The packet string in format "DATA|METHOD|CHECKSUM"
        debug: Whether to print debug messages (default: True)
        
    Returns:
        tuple: (corrupted_packet_str, original_data, corrupted_data, method, checksum, error_applied, error_method)
    """
    try:
        data_str, method, checksum = packet_str.rsplit("|", 2)
    except ValueError:
        raise ValueError("Invalid packet format. Expected 'DATA|METHOD|CHECKSUM'.")
    
    corrupted_data, error_method = corrupt_data_randomly(data_str, debug=debug)
    error_applied = (error_method != "none")
    
    corrupted_packet_str = f"{corrupted_data}|{method}|{checksum}"
    
    return corrupted_packet_str, data_str, corrupted_data, method, checksum, error_applied, error_method


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_sock:
        listen_sock.bind((LISTEN_HOST, LISTEN_PORT))
        listen_sock.listen(1)

        print(f"Server listening on: {LISTEN_HOST}:{LISTEN_PORT}")

        conn, addr = listen_sock.accept()
        with conn:
            print(f"Sender connected: {addr}")

            data = conn.recv(4096)
            if not data:
                print("Empty packet received, no processing.")
                return

            packet = data.decode("utf-8")
            print(f"Packet received from sender: {packet}")

            try:
                new_packet, data_str, corrupted_data, method, checksum, error_applied, error_method = process_packet(packet)
            except ValueError as e:
                print(str(e))
                return

            print(f"Original DATA: {data_str}")
            print(f"METHOD       : {method}")
            print(f"CHECKSUM     : {checksum}")
            print(f"Corrupted DATA: {corrupted_data}")
            print(f"Packet to be sent to receiver: {new_packet}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as out_sock:
                out_sock.connect((RECEIVER_HOST, RECEIVER_PORT))
                out_sock.sendall(new_packet.encode("utf-8"))
                print("Packet sent to receiver.")


if __name__ == "__main__":
    main()
