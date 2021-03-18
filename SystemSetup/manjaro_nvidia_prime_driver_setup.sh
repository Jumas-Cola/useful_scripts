#!/bin/bash
# Install nvidia driver
sudo mhwd -a pci nonfree 0300

# Set up a new Xorg configuration
mhwd_conf="/etc/X11/xorg.conf.d/90-mhwd.conf"
sudo rm $mhwd_conf
sudo touch $mhwd_conf
sudo cat > $mhwd_conf <<- EOM
Section "Module"
    Load "modesetting"
EndSection

Section "Device"
    Identifier "nvidia"
    Driver "nvidia"
    BusID "PCI:1:0:0"
    Option "AllowEmptyInitialConfiguration"
EndSection
EOM

# Refine blacklisting
sudo rm /etc/modprobe.d/mhwd*
nvidia_conf="/etc/modprobe.d/nvidia.conf"
sudo touch $nvidia_conf
sudo cat > $nvidia_conf <<- EOM
blacklist nouveau
blacklist nvidiafb
blacklist rivafb
EOM

# Enable nvidia-drm.modeset
nvidia_drm_conf="/etc/modprobe.d/nvidia-drm.conf"
sudo touch $nvidia_drm_conf
echo "options nvidia_drm modeset=1" >> $nvidia_drm_conf

# Set the output source for your DM
optimus_sh="/usr/local/bin/optimus.sh"
sudo touch $optimus_sh
sudo cat > $optimus_sh <<- EOM
#!/bin/sh
xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
EOM
sudo chmod a+rx /usr/local/bin/optimus.sh

reboot
