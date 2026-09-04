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
echo "you can start the server by typing in java -Xmx1000M -Xms100M -jar [name of server jar] in the minecraft-server directory"

