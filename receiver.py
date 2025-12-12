import socket
from error_methods import calculate_checksum

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 6000


def detect_error(packet_str: str) -> tuple[str, str, str, str, bool]:
    """
    Detect errors in a received packet by recomputing the checksum.
    
    Args:
        packet_str: The packet string in format "DATA|METHOD|CHECKSUM"
        
    Returns:
        tuple: (data_str, method, received_checksum, computed_checksum, error_detected)
    """
    try:
        data_str, method, received_checksum = packet_str.rsplit("|", 2)
    except ValueError:
        raise ValueError("Invalid packet format. Expected 'DATA|METHOD|CHECKSUM'.")
    
    data_bytes = data_str.encode("utf-8")
    computed_checksum = calculate_checksum(data_bytes, method)
    
    error_detected = (computed_checksum != received_checksum)
    
    return data_str, method, received_checksum, computed_checksum, error_detected


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
                data_str, method, received_checksum, computed_checksum, error_detected = detect_error(packet)
            except ValueError as e:
                print(str(e))
                return
                
            print(f"Received Data       : {data_str}")
            print(f"Method              : {method}")
            print(f"Sent Check Bits     : {received_checksum}")
            print(f"Computed Check Bits : {computed_checksum}")
            
            if error_detected:
                print("Error detected in the received data!")
            else:
                print("No error detected in the received data.")
if __name__ == "__main__":
    main()