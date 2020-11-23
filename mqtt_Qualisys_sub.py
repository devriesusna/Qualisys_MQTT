from time import sleep
import paho.mqtt.client as MQTT
import logging
import logging.handlers
from datetime import datetime
from gc import collect as trash
import json
import os
from config import *

DEBUGGING=1

#                       #
#-----Logging Setup-----#
#                       #
filename=datetime.now().strftime(default_folder+'mqtt_%Y%m%d_%H:%M:%s.log')
log = logging.getLogger()
log.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s : %(message)s')
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(format)
log.addHandler(file_handler)

#                       #
#-------MQTT Setup------#
#                       #
client=MQTT.Client(clientname)
topiclist=[
    'surf/#'
]

# basic callback for MQTT that prints message data directly.
def print_message(client,userdata,message):
	print()
	print("mqtt rx:")
	print(message.topic)
	#print(message.qos)
	print(message.payload)
	print(message.payload.decode())
	print(message.retain)
	print(client)

# A basic callback for MQTT that stores message data to a log file.
def log_message(client,userdata,message):
	log.info("message rx")
	log.info(str(message.topic)+", "+str(message.payload))

# The callback that our program will use to control device.
def process(client,userdata,message):
	#
	# Code to use the mqtt data.
	#
	a = 1

def check_quit():
	return 1

def setup_subscription():
	check=0
	try:
		# Connect to the server (defined by server.py)
		client.connect(mqtt_server)

		# Assigns the callback function when a mqtt message is received.
		if (DEBUGGING):
			client.on_message=print_message
		else:
			client.on_message=process

		# Subscribes to all the topics defined at top.
		for i in topiclist:
			client.subscribe(i)
			print("subscribed to: "+str(i))

		# Start the mqtt subscription.
		client.loop_start()
		print("Connected to MQTT server: "+mqtt_server)
		log.info("mqtt subscription script started")
		check=1
	except:
		print("didn't connect to MQTT server.")
		log.info("mqtt subscription failed")
	return check

def main():
	q=0
	# Run the MQTT setup once.
	q=setup_subscription()

	# Because the subscription works on interrupt callbacks, nothing happens in main.
	while(q):
		trash()
		sleep(1)
		q=check_quit()

main()




