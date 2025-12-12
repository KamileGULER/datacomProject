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


def corrupt_data_randomly(data: str) -> str:
   
    if not data:
        return data

    # 50% chance: no error
    if random.random() < 0.5:
        print("[DEBUG] No error applied.")
        return data

    methods = [
        char_substitution,
        char_deletion,
        char_insertion,
        char_swapping,
        flip_random_bit_in_char,
        multiple_bit_flips,
        burst_error,
    ]

    chosen_method = random.choice(methods)
    print(f"[DEBUG] Error method used: {chosen_method.__name__}")

    if chosen_method is multiple_bit_flips:
        return multiple_bit_flips(data, count=3)
    elif chosen_method is burst_error:
        return burst_error(data, length=3)
    else:
        return chosen_method(data)


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
                data_str, method, checksum = packet.rsplit("|", 2)
            except ValueError:
                print("Invalid packet format. Expected 'DATA|METHOD|CHECKSUM'.")
                return

            print(f"Original DATA: {data_str}")
            print(f"METHOD       : {method}")
            print(f"CHECKSUM     : {checksum}")

            corrupted_data = corrupt_data_randomly(data_str)
            print(f"Corrupted DATA: {corrupted_data}")

            new_packet = f"{corrupted_data}|{method}|{checksum}"
            print(f"Packet to be sent to receiver: {new_packet}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as out_sock:
                out_sock.connect((RECEIVER_HOST, RECEIVER_PORT))
                out_sock.sendall(new_packet.encode("utf-8"))
                print("Packet sent to receiver.")


if __name__ == "__main__":
    main()
