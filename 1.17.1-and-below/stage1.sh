apt update
apt upgrade -y
pkg install wget openssl-tool proot tar -y
pkg install python -y
hash -r
wget https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Scripts/Installer/Alpine/alpine.sh
bash alpine.sh
./start-alpine.sh

