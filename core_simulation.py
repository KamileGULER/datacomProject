"""
Core simulation logic that uses functions from sender.py, server.py, and receiver.py
for reuse in both CLI and web applications.

This module provides a unified interface to run the complete simulation
without requiring separate socket connections.
"""
from sender import create_packet
from server import process_packet
from receiver import detect_error


def simulate_sender(message: str) -> tuple[str, str, str]:
    """
    Simulate the sender behavior: calculate checksum and build packet.
    Uses the create_packet function from sender.py.
    
    Returns:
        tuple: (packet_str, method, checksum)
    """
    return create_packet(message, method="PARITY")


def simulate_server(packet_str: str) -> tuple[str, str, str, str, str, bool, str]:
    """
    Simulate the server behavior: receive packet, corrupt data, forward packet.
    Uses the process_packet function from server.py.
    
    Returns:
        tuple: (corrupted_packet_str, original_data, corrupted_data, method, checksum, error_applied, error_method)
    """
    return process_packet(packet_str, debug=False)


def simulate_receiver(packet_str: str) -> tuple[str, str, str, str, bool]:
    """
    Simulate the receiver behavior: receive packet, recompute checksum, detect error.
    Uses the detect_error function from receiver.py.
    
    Returns:
        tuple: (data_str, method, received_checksum, computed_checksum, error_detected)
    """
    return detect_error(packet_str)


def run_simulation(message: str) -> dict:
    """
    Run the complete simulation: Sender → Server → Receiver.
    
    Args:
        message: The original message to send
        
    Returns:
        dict: Complete simulation results with all relevant data
    """
    # Step 1: Sender
    original_packet, method, sent_checksum = simulate_sender(message)
    
    # Step 2: Server
    corrupted_packet, original_data, corrupted_data, _, _, error_applied, error_method = simulate_server(original_packet)
    
    # Step 3: Receiver
    received_data, _, received_checksum, computed_checksum, error_detected = simulate_receiver(corrupted_packet)
    
    # Determine final status
    status = "ERROR DETECTED" if error_detected else "NO ERROR DETECTED"
    
    return {
        "original_data": original_data,
        "original_packet": original_packet,
        "corrupted_data": corrupted_data,
        "corrupted_packet": corrupted_packet,
        "method": method,  # Should be "PARITY"
        "sent_checksum": sent_checksum,
        "computed_checksum": computed_checksum,
        "error_applied": error_applied,
        "error_method": error_method,
        "status": status,
        "received_data": received_data,  # Same as corrupted_data, but for clarity
    }

