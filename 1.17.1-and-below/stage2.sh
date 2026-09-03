#bin/bash

# Exit on error or missing dependencies
set -e

# Target GitHub repo details
REPO_USER="NBWgamer2012"
REPO_NAME="termux-minecraft-installation-tool"
TARGET_DIR="1.17.1-and-below"

# Ensure required commands are installed
for cmd in curl jq wget; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: '$cmd' is required but not installed."
        echo "Please install it using: pkg install $cmd (in Termux) or sudo apt install $cmd"
        exit 1
    fi
done

echo "Fetching available folders..."

# API URL to list directory contents
API_URL="https://api.github.com/repos/${REPO_USER}/${REPO_NAME}/contents/${TARGET_DIR}"

# Fetch API response and parse folder names into an array
mapfile -t FOLDERS < <(curl -s "$API_URL" | jq -r '.[] | select(.type=="dir") | .name')

if [ ${#FOLDERS[@]} -eq 0 ]; then
    echo "No folders found in $TARGET_DIR."
    exit 1
fi

echo ""
echo "Select a folder to download from:"
select FOLDER in "${FOLDERS[@]}"; do
    if [ -n "$FOLDER" ]; then
        echo "You selected: $FOLDER"
        break
    else
        echo "Invalid choice. Please pick a number from the list."
    fi
done

# Fetch download.txt raw contents directly from GitHub
RAW_URL="https://raw.githubusercontent.com/${REPO_USER}/${REPO_NAME}/main/${TARGET_DIR}/${FOLDER}/download.txt"

echo "Fetching download URL from download.txt..."
DOWNLOAD_URL=$(curl -s "$RAW_URL" | tr -d '\r' | xargs)

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Error: Could not retrieve a valid download URL from download.txt"
    exit 1
fi

echo "Downloading file from: $DOWNLOAD_URL"
wget "$DOWNLOAD_URL"

echo "Download completed!"
