apk update
apk upgrade
apk add openjdk8-jre-base
apk add nano
mkdir minecraft-server
wget https://github.com/NBWgamer2012/termux-minecraft-installation-tool/raw/refs/heads/main/1.17.1-and-below/versionselect.py
apk add python3
python3 versionselect.py
cd minecraft-server
wget https://github.com/NBWgamer2012/termux-minecraft-installation-tool/tree/main/thingy.txt
mv thingy.txt eula.txt
wget https://github.com/NBWgamer2012/termux-minecraft-installation-tool/raw/refs/heads/main/start.sh
chmod +x start.sh
echo "you can start the server by running start.sh in the minecraft-server directory"

