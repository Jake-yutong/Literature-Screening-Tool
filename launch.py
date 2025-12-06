#!/usr/bin/env python3
"""
Launcher script that starts the Flask server and opens the browser
"""
import time
import webbrowser
import socket
import threading
import sys

def is_port_in_use(port):
    """Check if a port is already in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0
    except:
        return False

def wait_for_server(port=5000, timeout=15):
    """Wait for the server to be ready"""
    print(f"Waiting for server to start on port {port}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.3)
    return False

def open_browser_delayed(url, delay=2):
    """Open browser after a delay"""
    time.sleep(delay)
    print(f"\nOpening browser: {url}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print(f"Please open this URL manually: {url}")

def main():
    port = 5000
    url = f'http://127.0.0.1:{port}'
    
    print("=" * 60)
    print("  Literature Screening Tool")
    print("=" * 60)
    print()
    
    # Check if port is already in use
    if is_port_in_use(port):
        print(f"Server is already running on port {port}!")
        print(f"Opening browser to {url}")
        webbrowser.open(url)
        print("\nPress Enter to exit...")
        input()
        return
    
    print("Starting Flask server...")
    print()
    
    # Start browser opener in background thread
    browser_thread = threading.Thread(target=open_browser_delayed, args=(url, 3))
    browser_thread.daemon = True
    browser_thread.start()
    
    # Import and run Flask app
    try:
        # Import the Flask app
        from app import app as flask_app
        
        print("=" * 60)
        print("  Server is starting...")
        print(f"  URL: {url}")
        print("  Press Ctrl+C to stop")
        print("=" * 60)
        print()
        
        # Start the Flask server (this is a blocking call)
        flask_app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
        
    except ImportError as e:
        print(f"\nError: Could not import app.py")
        print(f"Details: {e}")
        print("\nMake sure you are running this script from the correct directory.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"\nError starting server: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
