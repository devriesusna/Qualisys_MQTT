# Qualisys_MQTT
MQTT Publisher for Qualisys QTM Server
# Installation and Setup (Windows)
Install WSL using the instructions here:
https://docs.microsoft.com/en-us/windows/wsl/install-win10

Some things to do after their instructions:
'''
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-pip ipython3 mosquitto mosquitto-clients python3-paho-mqtt net-tools
python3 -m pip install qtm
'''
have to run mosquitto every new startup  – sudo service mosquitto start

To get mosquito running automatically at windows startup,
'sudo nano /etc/sudoers.d/README'

add line:
%sudo   ALL=(ALL) NOPASSWD: /usr/sbin/service mosquitto *

Winbutton+r : shell:startup
Create file autoexec.bat
Add line:
wsl sudo service mosquitto start

