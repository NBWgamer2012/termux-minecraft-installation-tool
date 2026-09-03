#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile


def ensure_root():
    """Ensure the script runs with root privileges."""
    if os.geteuid() != 0:
        print("[!] This script requires root privileges.")
        if subprocess.run(["which", "sudo"], capture_output=True).returncode == 0:
            print("[+] Re-running with sudo...\n")
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        else:
            print("[-] Please run this script as root (e.g., su - or sudo python script.py).")
            sys.exit(1)


REPO_USER = "NBWgamer2012"
REPO_NAME = "termux-minecraft-installation-tool"
TARGET_DIR = "1.17.1-and-below"


def main():
    ensure_root()

    api_url = f"https://api.github.com/repos/{REPO_USER}/{REPO_NAME}/contents/{TARGET_DIR}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})

    print("[+] Fetching available folders...")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"[-] Error fetching directory contents: {e}")
        sys.exit(1)

    folders = [item["name"] for item in data if item.get("type") == "dir"]

    if not folders:
        print(f"[-] No folders found in {TARGET_DIR}.")
        sys.exit(1)

    print("\nSelect a folder to download from:")
    for idx, folder in enumerate(folders, 1):
        print(f"{idx}) {folder}")

    choice = None
    while choice is None:
        try:
            selection = int(input("\nEnter choice number: "))
            if 1 <= selection <= len(folders):
                choice = folders[selection - 1]
            else:
                print("Invalid choice. Please pick a number from the list.")
        except ValueError:
            print("Please enter a valid integer.")

    print(f"\n[+] You selected: {choice}")

    raw_url = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/{TARGET_DIR}/{choice}/download.txt"
    raw_req = urllib.request.Request(raw_url, headers={"User-Agent": "Mozilla/5.0"})

    print("[+] Fetching download URL from download.txt...")
    try:
        with urllib.request.urlopen(raw_req) as response:
            download_url = response.read().decode().strip()
    except Exception as e:
        print(f"[-] Error reading download.txt: {e}")
        sys.exit(1)

    if not download_url:
        print("[-] Error: download.txt is empty.")
        sys.exit(1)

    # Determine filename from URL
    parsed_url = urllib.parse.urlparse(download_url)
    filename = os.path.basename(parsed_url.path) or "downloaded_file"
    current_dir = os.getcwd()

    print(f"[+] Downloading file as root to {current_dir}...")

    # Download using wget specifically into the current working directory
    subprocess.run(["wget", "-P", current_dir, download_url])

    filepath = os.path.join(current_dir, filename)

    # Check if the downloaded file is a zip archive
    if zipfile.is_zipfile(filepath):
        print(f"[+] '{filename}' is a zip archive. Unzipping...")
        try:
            with zipfile.ZipFile(filepath, "r") as zip_ref:
                zip_ref.extractall(current_dir)
            print("[+] Extraction complete.")

            # Optional: Clean up the original zip file after extracting
            os.remove(filepath)
            print(f"[+] Removed archive '{filename}'.")
        except Exception as e:
            print(f"[-] Failed to unzip file: {e}")
    else:
        print("[+] Download completed (file is not a zip archive).")


if __name__ == "__main__":
    main()