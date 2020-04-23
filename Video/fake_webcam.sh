#!/bin/bash
sudo modprobe -r v4l2loopback
cd "/home/$USER"
git clone https://github.com/umlaeute/v4l2loopback/
cd v4l2loopback
make && sudo make install
sudo depmod -a
sudo modprobe videodev
sudo insmod ./v4l2loopback.ko devices=1 video_nr=2 exclusive_caps=1
while :; do ffmpeg -re -i "$1" -map 0:v -f v4l2 /dev/video2; done
