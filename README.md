# AQI meter using PMS7003

## Design

 * Raspberry Pi reads data from sensor.
 * RBP runs telegraf to feed data into influxdb2.

TODO: RBP runs tiny webserver that displays basic metrics.

## Parts

 * Raspberry Pi
 * PMS7003 + adaptor
 
This post has the parts you'll need: https://joshefin.xyz/air-quality-with-raspberrypi-pms7003-and-java/ - also this is all heavily based on his work and instructions!

The adaptor I received had a "dupont" pinout and cabling already, so I didn't
need to do those steps. I just wired right to GPIO etc.

## Prework on SD card (in /boot)

### wifi

wpa_supplicant.conf:

```
country=us
update_config=1
ctrl_interface=/var/run/wpa_supplicant
network={
ssid="Your_SSID"
psk="Your_SSID"
}

```


### ssh

```
# this will be headless, so enable ssh
touch ssh
```

## Setup pi:

```
# Used for sensor script
sudo pip3 install pms7003

# used for sanity
sudo timedatectl set-timezone America/Los_Angeles

# This is so it will get its hostname from DHCP
sudo hostnamectl set-hostname localhost

# We're going to use the serial port for the sensor, so disable the serial
# console.
sudo raspi-config
# In Interfacing Options > Serial section, disable the serial login shell
# and enable the serial interface.

# needed for telegraf
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update
sudo apt-get install telegraf

# needed so telegraf can read/write serial device
sudo usermod -a -G dialout telegraf

cd
git clone https://github.com/c6rbon/AQI.git

# Edit telegraf.conf with your own influxdb2 credentials, or whatever output
# you like.

sudo cp telegraf.conf
sudo systemctl reload telegraf
```

