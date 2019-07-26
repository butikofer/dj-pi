DJ Pi
=====

A simple Python script that uses `scapy` to listen for Amazon Dash button
activation and then triggers playing a random MP3 file from a configured
directory. This music plays, by default, to the miniplug audio output of the 
Raspberry Pi.

I used https://www.raspberrypi.org/magpi/hack-amazon-dash-button-raspberry-pi/ as a starting point.

Install
-------

* Setup Amazon Dash button to be used as IoT device on your WiFi network. (See https://www.raspberrypi.org/magpi/hack-amazon-dash-button-raspberry-pi/ for more info.)
* Install `scapy` Python library: `sudo apt-get install python-scapy`
* Modify script to point to the correct directory for audio files and the Dash button MAC address
* Execute script as root: `sudo ./dj-pi.py` 
* You can copy the SysV start-up script to `/etc/init.d/` and then symlink it into `/etc/rc3.d/` to ensure that the script starts up upon boot


Bluetooth
---------

These notes explain what I attempted to do in order to get Bluetooth working with the Pi.
This turned out being difficult to do ... at least with an Amazon Echo. PulseAudio didn't always
work and the Bluetooth pairing was flaky. In the end, I gave up on this given the amount of time
it was taking

```
sudo apt install pavucontrol -y
sudo reboot
sudo apt-get install mpg123
```

Need to first pair with Bluetooth speaker:
```
bluetoothctl
power on
agent on
discover on
pair XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX
```

Start up sound to play the MP3 file (didn't always work):
```
pulseaudio --start
echo -e 'connect 44:65:0D:FB:E5:38\nquit' | sudo bluetoothctl
pacmd set-default-sink 1
mpg123 example.mp3 
```
