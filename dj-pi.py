#!/usr/bin/python

import time, os, random, subprocess, logging, sys

if len(sys.argv) < 2 or (sys.argv[1] != "start" and sys.argv[1] != "stop"):
	print "USAGE: dj-pi.py [start | stop]"
	sys.exit(1)

if sys.argv[1] == "stop":
	print "Stopping..."
	sys.exit(0)

from scapy.all import *

# Where the audio files are located
AUDIO_FILES_DIR="/home/pi/dj-pi/audio-files"

# The MAC address of the Amazon Dash button
MAC_ADDR="40:B4:CD:27:E1:12"

# Waiting period (in seconds) to avoid detecting a phantom double button press
TIMEOUT=2

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

logging.info("Starting up DJ PI...")

last_detect_time = 0
def arp_detect(pkt):
	global last_detect_time
	if ARP not in pkt:
		return
	if pkt[ARP].op == 1: #network request
		if pkt[ARP].hwsrc == MAC_ADDR.lower():
			if time.time() - last_detect_time > TIMEOUT: 
				last_detect_time = time.time()
				# Get random audio file to play
				file_name = AUDIO_FILES_DIR + "/" + random.choice(list(filter(lambda x: not x.startswith("."), os.listdir(AUDIO_FILES_DIR))))
				logging.warning("Button detected. Playing '%s'" % (file_name))
				result = subprocess.call(["omxplayer", file_name])
				logging.warning("Played file with %d result" % (result))
			else:
				logging.info("Duplicate button press detected--not playing audio")
        
logging.warning(sniff(prn=arp_detect, filter="arp", store=0))
