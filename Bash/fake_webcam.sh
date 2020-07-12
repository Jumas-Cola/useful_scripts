#!/bin/bash
#_____INSTALLATION_____
sudo modprobe -r v4l2loopback
cd "/home/$USER"
git clone https://github.com/umlaeute/v4l2loopback/
cd v4l2loopback
make && sudo make install


#_____USAGE_____
sudo modprobe -r v4l2loopback
sudo depmod -a
sudo modprobe v4l2loopback video_nr=2,3,4 exclusive_caps=1,1,1
while :; do ffmpeg -re -i "/home/Video/video1.mp4" -map 0:v -f v4l2 /dev/video2; done &
while :; do ffmpeg -re -i "/home/Video/video2.mp4" -map 0:v -f v4l2 /dev/video3; done &
while :; do ffmpeg -re -i "/home/Video/video3.mp4" -map 0:v -f v4l2 /dev/video4; done
