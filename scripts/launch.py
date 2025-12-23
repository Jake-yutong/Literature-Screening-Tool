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

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

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
    requested_port = 5000
    
    print("=" * 60)
    print("  Literature Screening Tool")
    print("=" * 60)
    print()
    
    # Check if port is already in use, if so check if server is responding
    if is_port_in_use(requested_port):
        print(f"Port {requested_port} is already in use.")
        print("Checking if it's our server...")
        # Try to connect to see if it's responding
        try:
            import urllib.request
            urllib.request.urlopen(f'http://127.0.0.1:{requested_port}', timeout=1)
            print(f"Server is already running on port {requested_port}!")
            print(f"Opening browser to http://127.0.0.1:{requested_port}")
            webbrowser.open(f'http://127.0.0.1:{requested_port}')
            print("\nPress Enter to exit...")
            input()
            return
        except:
            pass
    
    # Find an available port
    port = find_available_port(requested_port)
    if port is None:
        print("\n❌ Error: Could not find an available port")
        print("   Please close other programs or check your firewall settings")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    if port != requested_port:
        print(f"\n⚠️  Port {requested_port} is in use by another program")
        print(f"   Automatically switched to port {port}")
        if requested_port == 5000:
            print("\n💡 Tip: On macOS, you can disable AirPlay Receiver in")
            print("   System Settings → General → AirPlay Receiver")
        print()
    
    url = f'http://127.0.0.1:{port}'
    
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
