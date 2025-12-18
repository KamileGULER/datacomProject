import socket
from error_methods import calculate_checksum
import random

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

SUPPORTED_METHODS = [
    "PARITY",
    "PARITY_ODD",
    "2D_PARITY",
    "CRC16",
    "CRC32",
    "INTERNET_CHECKSUM",
]

def create_packet(message: str, method: str ) -> tuple[str, str, str]:
    method = method.strip().upper()
    if "|" in message:
        raise ValueError("Message cannot contain the '|' character.")
    data_bytes = message.encode("utf-8")
    checksum = calculate_checksum(data_bytes, method)
    packet_str = f"{message}|{method}|{checksum}"
    return packet_str, method, checksum


def send_packet_to_server(packet_str: str, host: str = SERVER_HOST, port: int = SERVER_PORT) -> bool:
  
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(packet_str.encode("utf-8"))
            return True
    except ConnectionRefusedError:
        print("Could not connect to server. server.py is probably not running.")
        return False
    except OSError as e:
        print(f"Connection error: {e}")
        return False


def main():
    data_str = input("Enter the message to send: ")

    method = random.choice(SUPPORTED_METHODS)
    packet_str, method, checksum = create_packet(data_str, method)

    print(f"Chosen METHOD     : {method}")
    print(f"Packet to be sent : {packet_str}")

    if send_packet_to_server(packet_str):
        print("Packet sent to server.")

if __name__ == "__main__":
    main()
