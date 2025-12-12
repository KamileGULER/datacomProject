# Data Communication Simulation Project

A Python project that simulates a data communication system with error detection using parity checking. The project includes both CLI and web-based interfaces.

## Project Structure

- **`sender.py`** - CLI client that sends messages to the server
  - Contains `create_packet()` function for packet creation
  - Contains `send_packet_to_server()` function for socket communication
- **`server.py`** - CLI server that receives messages, applies error injection, and forwards to receiver
  - Contains error injection methods (`char_substitution`, `bit_flip`, etc.)
  - Contains `corrupt_data_randomly()` and `process_packet()` functions
- **`receiver.py`** - CLI client that receives messages and detects errors
  - Contains `detect_error()` function for error detection
- **`error_methods.py`** - Core parity calculation logic (single source of truth)
- **`core_simulation.py`** - Unified simulation interface that imports from sender.py, server.py, and receiver.py
  - Used by web app to run complete simulations
  - Ensures CLI and web use the exact same logic
- **`web_app.py`** - Flask web application with modern UI
- **`templates/index.html`** - Modern dark-themed web interface

## Features

- **Parity-based error detection** - Uses even parity bit calculation
- **Multiple error injection methods**:
  - Character substitution
  - Character deletion
  - Character insertion
  - Character swapping
  - Bit flip
  - Multiple bit flips
  - Burst error
- **Modern web UI** - Dark-themed interface showing Sender → Server → Receiver flow
- **CLI support** - Original terminal-based workflow still works

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)

1. Start the web application:
```bash
python web_app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8080
```

3. Enter a message in the input field and click "Send" to run the simulation.

The UI will display:
- **Sender (Client 1)**: Original data, method, checksum, and packet
- **Server (Error Injection)**: Corrupted data, error method applied, and forwarded packet
- **Receiver (Client 2)**: Received data, computed checksum, and final status

### CLI Interface (Original)

To use the original CLI workflow:

1. **Terminal 1** - Start the server:
```bash
python server.py
```

2. **Terminal 2** - Start the receiver:
```bash
python receiver.py
```

3. **Terminal 3** - Start the sender:
```bash
python sender.py
```

Enter a message when prompted. The sender will send it to the server, which will corrupt it (50% chance) and forward to the receiver for error detection.

## How It Works

1. **Sender** calculates an even parity bit over the entire message using `calculate_checksum()` from `error_methods.py`
2. **Packet format**: `DATA|METHOD|CONTROL` where:
   - `DATA` = original message
   - `METHOD` = `"PARITY"`
   - `CONTROL` = parity bit (`"0"` or `"1"`)
3. **Server** receives the packet, corrupts the DATA field (50% chance), and forwards to Receiver
4. **Receiver** recomputes the parity bit and compares with the received checksum to detect errors

## Error Detection

- If computed checksum matches received checksum → **NO ERROR DETECTED** (green)
- If computed checksum differs from received checksum → **ERROR DETECTED** (red)

Note: Parity checking can detect single-bit errors but may miss some multi-bit errors.

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Protocol**: TCP sockets (for CLI) / HTTP REST API (for web)
- **Ports**: 
  - Server listens on `127.0.0.1:5000` (CLI)
  - Receiver listens on `127.0.0.1:6000` (CLI)
  - Web app runs on `127.0.0.1:8080`

## Architecture & Design

### Code Organization

The project follows a **refactored architecture** where:

1. **Core Logic Functions**: Each module (`sender.py`, `server.py`, `receiver.py`) exports reusable functions:
   - `sender.create_packet()` - Creates packets with checksum
   - `server.process_packet()` - Processes and corrupts packets
   - `receiver.detect_error()` - Detects errors in received packets

2. **CLI Usage**: The original `main()` functions in each file use these functions, maintaining backward compatibility

3. **Web Usage**: `core_simulation.py` imports and uses the same functions, ensuring:
   - **Single source of truth** - No code duplication
   - **Consistency** - CLI and web use identical logic
   - **Maintainability** - Changes in one place affect both interfaces

### Benefits

- ✅ **No code duplication** - Logic defined once, used everywhere
- ✅ **Single source of truth** - `error_methods.py` for parity, module functions for operations
- ✅ **Backward compatible** - CLI still works exactly as before
- ✅ **Professional structure** - Clean separation of concerns
- ✅ **Easy to extend** - New features can be added to functions, automatically available everywhere

