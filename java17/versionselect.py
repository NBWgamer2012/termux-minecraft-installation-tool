#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile

BASE_SAVE_DIR = "/root/minecraft-server"
REPO_USER = "NBWgamer2012"
REPO_NAME = "termux-minecraft-installation-tool"
TARGET_DIR = "java17"


def main():
    api_url = f"https://api.github.com/repos/{REPO_USER}/{REPO_NAME}/contents/{TARGET_DIR}"
    req = urllib.request.Request(
        api_url, headers={"User-Agent": "Mozilla/5.0"}
    )

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

    # Set destination directory to /root/minecraft-server/<selected_option>
    target_save_dir = os.path.join(BASE_SAVE_DIR, choice)
    
    try:
        os.makedirs(target_save_dir, exist_ok=True)
    except PermissionError:
        print(f"[-] Permission denied when creating {target_save_dir}.")
        print("[-] Please ensure you run this script with root privileges.")
        sys.exit(1)

    raw_url = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/{TARGET_DIR}/{choice}/download.txt"
    raw_req = urllib.request.Request(
        raw_url, headers={"User-Agent": "Mozilla/5.0"}
    )

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

    parsed_url = urllib.parse.urlparse(download_url)
    filename = os.path.basename(parsed_url.path) or "downloaded_file"
    filepath = os.path.join(target_save_dir, filename)

    print(f"[+] Downloading file to {target_save_dir}...")

    subprocess.run(["wget", "-P", target_save_dir, download_url])

    if filename.lower().endswith(".zip"):
        print(f"[+] '{filename}' has a .zip extension. Unzipping...")
        try:
            with zipfile.ZipFile(filepath, "r") as zip_ref:
                zip_ref.extractall(target_save_dir)
            print("[+] Extraction complete.")

            os.remove(filepath)
            print(f"[+] Removed archive '{filename}'.")
        except Exception as e:
            print(f"[-] Failed to unzip file: {e}")
    else:
        print(f"[+] Download completed (kept '{filename}' as-is).")


if __name__ == "__main__":
    main()