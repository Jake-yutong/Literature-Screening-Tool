#!/usr/bin/env python3
"""
Launcher script that starts the Flask server and opens the browser
"""
import subprocess
import time
import webbrowser
import socket
import sys
import os

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def wait_for_server(host='127.0.0.1', port=5000, timeout=30):
    """Wait for the server to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.5)
    return False

def main():
    port = 5000
    url = f'http://127.0.0.1:{port}'
    
    print("=" * 60)
    print("  Literature Screening Tool")
    print("=" * 60)
    print()
    
    # Check if port is already in use
    if is_port_in_use(port):
        print(f"⚠ Port {port} is already in use!")
        print(f"Opening browser to {url}")
        webbrowser.open(url)
        input("\nPress Enter to exit...")
        return
    
    # Start Flask server in a subprocess
    print("Starting Flask server...")
    
    # Determine the correct Python command
    python_cmd = sys.executable
    
    # Start the server
    server_process = subprocess.Popen(
        [python_cmd, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Wait for server to be ready
    print(f"Waiting for server on {url}...")
    
    if wait_for_server(port=port):
        print(f"✓ Server is ready!")
        print(f"✓ Opening browser to {url}")
        time.sleep(0.5)  # Small delay to ensure server is fully ready
        webbrowser.open(url)
        print()
        print("=" * 60)
        print("  Server is running!")
        print(f"  Access at: {url}")
        print("  Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
        
        # Stream server output
        try:
            for line in server_process.stdout:
                print(line, end='')
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            server_process.terminate()
            server_process.wait()
            print("Server stopped.")
    else:
        print("✗ Server failed to start within timeout period")
        print("\nServer output:")
        print("-" * 60)
        output, _ = server_process.communicate(timeout=5)
        print(output)
        server_process.terminate()
    
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        input("\nPress Enter to exit...")
