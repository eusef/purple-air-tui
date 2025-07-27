import json
import requests
import time
import socket
from typing import Callable


HOSTNAME_URL = "http://purpleair-1a9c/json"

# Config
POLL_INTERVAL_SECONDS = 5
TIMEOUT_SECONDS = 5


def test_network_connectivity():
    """Test basic network connectivity to help debug issues"""
    print("=== NETWORK CONNECTIVITY TEST ===")
    
    # Test DNS resolution
    for url in [HOSTNAME_URL]:
        try:
            hostname = url.split("//")[1].split("/")[0]
            if ":" in hostname:
                hostname = hostname.split(":")[0]
            print(f"Testing DNS resolution for: {hostname}")
            ip = socket.gethostbyname(hostname)
            print(f"✓ Resolved to: {ip}")
        except socket.gaierror as e:
            print(f"✗ DNS resolution failed: {e}")
    
    # Test HTTP connectivity
    for url in [HOSTNAME_URL]:
        print(f"\nTesting HTTP connectivity to: {url}")
        try:
            start_time = time.time()
            resp = requests.get(url, timeout=5)
            request_time = time.time() - start_time
            print(f"✓ HTTP request successful")
            print(f"  Status: {resp.status_code}")
            print(f"  Response time: {request_time:.2f}s")
            print(f"  Content length: {len(resp.content)} bytes")
        except requests.exceptions.ReadTimeout:
            print(f"✗ Timeout after 5 seconds")
        except requests.exceptions.ConnectionError as e:
            print(f"✗ Connection error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    print("\n=== END NETWORK TEST ===")


def poll_sensor(callback: Callable[[dict], None], interval: float = POLL_INTERVAL_SECONDS):
    """
    Poll PurpleAir sensor via HTTP and send JSON data to callback.
    Tries hostname first, then falls back to static IP on error.
    """
    last_url = HOSTNAME_URL
    attempt_count = 0

    while True:
        attempt_count += 1
        try:
            print(f"[DEBUG] Attempt {attempt_count}: Polling {last_url}")
            print(f"[DEBUG] Timeout set to {TIMEOUT_SECONDS} seconds")
            
            # Test DNS resolution first
            import socket
            try:
                hostname = last_url.split("//")[1].split("/")[0]
                if ":" in hostname:
                    hostname = hostname.split(":")[0]
                print(f"[DEBUG] Resolving hostname: {hostname}")
                ip = socket.gethostbyname(hostname)
                print(f"[DEBUG] Resolved to IP: {ip}")
            except socket.gaierror as e:
                print(f"[DEBUG] DNS resolution failed: {e}")
                callback({"error": f"DNS resolution failed for {hostname}: {e}"})
                last_url = HOSTNAME_URL
                time.sleep(interval)
                continue
            
            print(f"[DEBUG] Making HTTP request...")
            start_time = time.time()
            resp = requests.get(last_url, timeout=TIMEOUT_SECONDS)
            request_time = time.time() - start_time
            print(f"[DEBUG] Request completed in {request_time:.2f} seconds")
            print(f"[DEBUG] Response status: {resp.status_code}")
            
            resp.raise_for_status()
            print(f"[DEBUG] Parsing JSON response...")
            data = resp.json()
            print(f"[DEBUG] JSON parsed successfully, keys: {list(data.keys())}")
            callback(data)
            
        except requests.exceptions.ReadTimeout:
            print(f"[ERROR] Timeout after {TIMEOUT_SECONDS}s from {last_url}")
            print(f"[DEBUG] This could indicate:")
            print(f"[DEBUG] - Network connectivity issues")
            print(f"[DEBUG] - Firewall blocking the connection")
            print(f"[DEBUG] - PurpleAir sensor is offline")
            callback({"error": f"Timeout after {TIMEOUT_SECONDS}s from {last_url}"})
        except requests.exceptions.ConnectionError as e:
            print(f"[ERROR] Connection error: {e}")
            print(f"[DEBUG] This could indicate:")
            print(f"[DEBUG] - PurpleAir sensor is not reachable at this address")
            print(f"[DEBUG] - Network routing issues")
            print(f"[DEBUG] - Wrong IP address or hostname")
            callback({"error": f"Connection error: {e}"})
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            print(f"[DEBUG] Error type: {type(e).__name__}")
            callback({"error": str(e)})
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            print(f"[DEBUG] Error type: {type(e).__name__}")
            callback({"error": f"Unexpected error: {e}"})

        
        old_url = last_url
        last_url = HOSTNAME_URL
        print(f"[DEBUG] Switching from {old_url} to {last_url}")
        
        print(f"[DEBUG] Waiting {interval} seconds before next attempt...")
        time.sleep(interval)

# Entry point for standalone testing
if __name__ == "__main__":
    def print_callback(data):
        print("[RAW JSON]", json.dumps(data, indent=2))
    
    # Run network test first
    test_network_connectivity()
    
    print("\nStarting sensor polling...")
    try:
        poll_sensor(print_callback)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")