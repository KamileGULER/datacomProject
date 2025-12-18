from __future__ import annotations
import random
from sender import create_packet, SUPPORTED_METHODS
from server import process_packet
from receiver import detect_error

def simulate_sender(message: str, method: str | None = None) -> tuple[str, str, str]:
    chosen_method = (method or random.choice(SUPPORTED_METHODS)).strip().upper()
    return create_packet(message, chosen_method)    


def simulate_server(packet_str: str) -> tuple[str, str, str, str, str, bool, str]:
    return process_packet(packet_str, debug=False)


def simulate_receiver(packet_str: str) -> tuple[str, str, str, str, bool]:
    return detect_error(packet_str)


def run_simulation(message: str, method: str | None = None) -> dict:
    # Step 1: Sender
    original_packet, method_used, sent_checksum = simulate_sender(message, method)
    
    # Step 2: Server
    (corrupted_packet, original_data, corrupted_data,
    method_srv, checksum_srv, error_applied, error_method) = simulate_server(original_packet)    
    # Step 3: Receiver
    received_data, method_rx, received_checksum, computed_checksum, error_detected = simulate_receiver(corrupted_packet)
    
    # Determine final status
    status = "ERROR DETECTED" if error_detected else "NO ERROR DETECTED"
    
    return {
        "original_data": original_data,
        "original_packet": original_packet,
        "corrupted_data": corrupted_data,
        "corrupted_packet": corrupted_packet,

        "method": method_used,
        "method_server": method_srv,
        "method_receiver": method_rx,

        "sent_checksum": sent_checksum,
        "sent_checksum_after_server": checksum_srv, 
        "computed_checksum": computed_checksum,

        "error_applied": error_applied,
        "error_method": error_method,
        "status": status,
        "received_data": received_data,
        "received_checksum": received_checksum,
    }

