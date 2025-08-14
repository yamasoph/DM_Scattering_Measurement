#!/bin/sh
# launcher.sh

cd /home/locsst/code/camera
sudo touch Logging.txt
sudo rm Logging.txt
sudo touch Logging.txt
sudo python3 dm_Driver.py > Logging.txt