import socket
from error_methods import calculate_checksum

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def main():
    data_str = input("Enter the message to send: ")

    method = "PARITY"
    data_bytes = data_str.encode("utf-8")

    checksum = calculate_checksum(data_bytes, method)

    packet_str = f"{data_str}|{method}|{checksum}"
    print(f"Packet to be sent: {packet_str}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_HOST, SERVER_PORT))
            sock.sendall(packet_str.encode("utf-8"))
            print("Packet sent to server.")
    except ConnectionRefusedError:
        print("Could not connect to server. server.py is probably not running.")
    except OSError as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    main()
