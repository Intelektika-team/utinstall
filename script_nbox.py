#!/usr/bin/env python3
import os
import sys
import socket
import subprocess
import platform
import urllib.request
import time
import re
import ssl
import hashlib
import base64
import zipfile
import json
from datetime import datetime
 
def print_help():
    print("""
Hacker Multi-Tool v2.0 (macOS)
Usage: python3 script.py <function_number>

Available functions:
0 - Help (this message)
1 - Wi-Fi scanner (current networks)
2 - Check external IP
3 - Ping sweep local network
4 - Scan open ports on localhost
5 - Check internet connection
6 - System information
7 - ARP scanner (requires sudo)
8 - DNS resolver
9 - Directory lister
10 - File hasher
11 - Base64 encoder/decoder
12 - Simple port listener
13 - Process lister
14 - Network interfaces info
15 - SSL checker for websites
16 - Password generator
17 - File search by pattern
18 - Clipboard stealer (macOS)
19 - System clipboard manager
20 - Screenshot taker (macOS)
""")

def wifi_scanner():
    print("[*] Scanning Wi-Fi networks...")
    try:
        result = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"], 
                              capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"[!] Error: {e}")

def check_external_ip():
    print("[*] Checking external IP...")
    try:
        with urllib.request.urlopen("https://api.ipify.org") as response:
            print(f"Your external IP: {response.read().decode('utf-8')}")
    except Exception as e:
        print(f"[!] Error: {e}")

def ping_sweep():
    print("[*] Pinging all devices in local network...")
    try:
        base_ip = ".".join(socket.gethostbyname(socket.gethostname()).split(".")[:3]) + "."
        for i in range(1, 255):
            ip = base_ip + str(i)
            res = subprocess.call(["ping", "-c", "1", "-W", "200", ip], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res == 0:
                print(f"[+] {ip} is alive")
    except Exception as e:
        print(f"[!] Error: {e}")

def port_scanner():
    print("[*] Scanning open ports on localhost...")
    try:
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                print(f"Port {port} is open")
            sock.close()
    except Exception as e:
        print(f"[!] Error: {e}")

def check_internet():
    print("[*] Checking internet connection...")
    try:
        urllib.request.urlopen("https://google.com", timeout=5)
        print("[+] Internet connection is active")
    except:
        print("[!] No internet connection")

def system_info():
    print("[*] System information:")
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"Local IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python version: {platform.python_version()}")

def arp_scan():
    print("[*] ARP scanning local network...")
    try:
        if os.geteuid() != 0:
            print("[!] Requires sudo privileges")
            return
            
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"[!] Error: {e}")

def dns_resolver():
    print("[*] DNS resolver - enter hostnames separated by commas")
    try:
        hostnames = "google.com,github.com,example.com".split(",")  # Default example
        for host in hostnames:
            try:
                ip = socket.gethostbyname(host.strip())
                print(f"{host} -> {ip}")
            except socket.gaierror:
                print(f"{host} -> Cannot resolve")
    except Exception as e:
        print(f"[!] Error: {e}")

def directory_lister():
    print("[*] Listing current directory with details")
    try:
        for item in os.listdir('.'):
            stats = os.stat(item)
            print(f"{item} | Size: {stats.st_size} bytes | Modified: {datetime.fromtimestamp(stats.st_mtime)}")
    except Exception as e:
        print(f"[!] Error: {e}")

def file_hasher():
    print("[*] File hasher - calculates MD5, SHA1, SHA256")
    try:
        files = [f for f in os.listdir('.') if os.path.isfile(f)][:5]  # First 5 files
        for file in files:
            with open(file, 'rb') as f:
                data = f.read()
                print(f"\nFile: {file}")
                print(f"MD5: {hashlib.md5(data).hexdigest()}")
                print(f"SHA1: {hashlib.sha1(data).hexdigest()}")
                print(f"SHA256: {hashlib.sha256(data).hexdigest()}")
    except Exception as e:
        print(f"[!] Error: {e}")

def base64_tool():
    print("[*] Base64 encoder/decoder")
    try:
        sample_text = "sample text for encoding"
        encoded = base64.b64encode(sample_text.encode()).decode()
        decoded = base64.b64decode(encoded.encode()).decode()
        print(f"Original: {sample_text}")
        print(f"Encoded: {encoded}")
        print(f"Decoded: {decoded}")
    except Exception as e:
        print(f"[!] Error: {e}")

def port_listener():
    print("[*] Simple port listener on port 12345 (CTRL+C to stop)")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', 12345))
            s.listen(1)
            print("Listening on port 12345...")
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data.decode()}")
    except Exception as e:
        print(f"[!] Error: {e}")

def process_lister():
    print("[*] Running processes:")
    try:
        result = subprocess.run(["ps", "-aux"], capture_output=True, text=True)
        print(result.stdout[:1000] + "...")  # Show first 1000 chars
    except Exception as e:
        print(f"[!] Error: {e}")

def network_interfaces():
    print("[*] Network interfaces information:")
    try:
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"[!] Error: {e}")

def ssl_checker():
    print("[*] SSL certificate checker for google.com:443")
    try:
        hostname = "google.com"
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"SSL Certificate for {hostname}:")
                print(f"Issuer: {cert['issuer']}")
                print(f"Valid from: {cert['notBefore']}")
                print(f"Valid until: {cert['notAfter']}")
    except Exception as e:
        print(f"[!] Error: {e}")

def password_generator():
    print("[*] Generating 5 random password examples")
    try:
        for _ in range(5):
            random_bytes = os.urandom(8)
            password = base64.b64encode(random_bytes).decode('utf-8')[:12]
            print(f"Password: {password}")
    except Exception as e:
        print(f"[!] Error: {e}")

def file_search():
    print("[*] Searching for .txt files in current directory")
    try:
        for root, _, files in os.walk('.'):
            for file in files:
                if file.endswith('.txt'):
                    print(f"Found: {os.path.join(root, file)}")
    except Exception as e:
        print(f"[!] Error: {e}")

def clipboard_stealer():
    print("[*] Reading macOS clipboard (requires pbpaste)")
    try:
        result = subprocess.run(["pbpaste"], capture_output=True, text=True)
        print(f"Clipboard content:\n{result.stdout}")
    except Exception as e:
        print(f"[!] Error: {e}")

def clipboard_manager():
    print("[*] Setting clipboard to 'hacked' (requires pbcopy)")
    try:
        subprocess.run(["pbcopy"], input="hacked", text=True)
        print("Clipboard set to 'hacked'")
    except Exception as e:
        print(f"[!] Error: {e}")

def take_screenshot():
    print("[*] Taking screenshot (requires screencapture)")
    try:
        filename = f"screenshot_{int(time.time())}.png"
        subprocess.run(["screencapture", filename])
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"[!] Error: {e}")

def main(option):
    functions = {
        "0": print_help,
        "1": wifi_scanner,
        "2": check_external_ip,
        "3": ping_sweep,
        "4": port_scanner,
        "5": check_internet,
        "6": system_info,
        "7": arp_scan,
        "8": dns_resolver,
        "9": directory_lister,
        "10": file_hasher,
        "11": base64_tool,
        "12": port_listener,
        "13": process_lister,
        "14": network_interfaces,
        "15": ssl_checker,
        "16": password_generator,
        "17": file_search,
        "18": clipboard_stealer,
        "19": clipboard_manager,
        "20": take_screenshot
    }

    if option in functions:
        functions[option]()
    else:
        print("[!] Invalid function number. Use 0 for help.")
