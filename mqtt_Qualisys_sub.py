from time import sleep
import paho.mqtt.client as MQTT
from gc import collect as trash
import json

DEBUGGING=1


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect, return code: ", rc)



# basic callback for MQTT that prints message data directly.
def print_message(client,userdata,message):
	print()
	print("mqtt rx:")
	print(message.topic)
	print(message.qos)
	# print(message.payload)
	print(message.payload.decode())
	print(message.retain)
	# print(client)


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
		client.connect(broker_address,port)

		# Assigns the callback function when a mqtt message is received.
		if (DEBUGGING):
			client.on_message=print_message
		else:
			client.on_message=process

		# Subscribes to all the topics defined at top.
		for i in topiclist:
			client.subscribe(i+'/'+'#')

		# Start the mqtt subscription.
		client.loop_start()
		check=1
	except:
		print("didn't connect")
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


#                       #
#-------MQTT Setup------#
#                       #
client=MQTT.Client()
client.on_connect = on_connect
topiclist=['poseDCM', 'poseEul']

# Connect to MQTT broker
broker_address = "10.24.6.23"
port = 1883

main()




