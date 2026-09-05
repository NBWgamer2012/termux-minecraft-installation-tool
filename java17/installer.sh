apt update
apt upgrade -y
pkg install wget -y
pkg install python3 -y
pkg install openjdk-17 -y
mkdir minecraft-server 
wget https://github.com/NBWgamer2012/termux-minecraft-installation-tool/raw/refs/heads/main/java17/versionselect.py
python3 versionselect.py
cd minecraft-server