import socket
from error_methods import calculate_checksum

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000


def create_packet(message: str, method: str = "PARITY") -> tuple[str, str, str]:
    
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

    packet_str, method, checksum = create_packet(data_str)
    print(f"Packet to be sent: {packet_str}")

    if send_packet_to_server(packet_str):
        print("Packet sent to server.")

if __name__ == "__main__":
    main()
