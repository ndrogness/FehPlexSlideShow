# FehPlexSlideShow
Python wrapper for feh slideshow using your Plex photos media

Concept taken from https://www.raspberrypi.org/forums/viewtopic.php?t=199320

This was built to run on a Raspberry Pi but could be used on other system.
Note: this should installed in /home/pi/FehPlexSlideShow
cd ~pi && git clone https://github.com/ndrogness/FehPlexSlideShow.git

#Here are prerequisite packages/modules:
sudo apt-get install imagemagick
sudo apt-get install feh
sudo apt-get install xscreensaver
sudo pip3 install plexapi

# Auto run on Pi Desktop using autologin with username pi:
Turn off screensaver (Under Preference - xscreensaver preferences to turn off the screensaver entirely.

chmod 755 /home/pi/FehPlexSlideShow/AutoRun.sh

Add the following line to the file /home/pi/.config/lxsession/LXDE-pi/autostart:
@/bin/sh /home/pi/FehPlexSlideShow/AutoRun.sh
