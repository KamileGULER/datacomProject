import socket
from error_methods import calculate_checksum
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 6000
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock: 
        server_sock.bind((LISTEN_HOST, LISTEN_PORT))
        server_sock.listen(1)
        print(f"Listening on {LISTEN_HOST}:{LISTEN_PORT}...")
        conn, addr = server_sock.accept()
        with conn:
            print(f"Server is connected : {addr}")
            data = conn.recv(4096)
            if not data:
                print("Empty package arrived.")
                return
            packet = data.decode("utf-8")
            print(f"Received package: {packet}")
            try:
                data_str, method, received_checksum = packet.rsplit("|", 2)
            except ValueError:
                print("Invalid packet format.")
                return
            data_bytes = data_str.encode("utf-8")
            computed_control = calculate_checksum(data_bytes, method)
            print(f"Received Data       : {data_str}")
            print(f"Method              : {method}")
            print(f"Sent Check Bits     : {received_checksum}")
            print(f"Computed Check Bits : {computed_control}")
            if computed_control == received_checksum:
                print("No error detected in the received data.")
            else:
                print("Error detected in the received data!")
if __name__ == "__main__":
    main()