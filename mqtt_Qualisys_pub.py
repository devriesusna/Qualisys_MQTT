import json
from time import sleep
from datetime import datetime
import paho.mqtt.client as MQTT
from gc import collect as trash
import asyncio
import qtm
import xml.etree.ElementTree as ET
from config import *
from math import isnan

DEBUGGING=1

client = MQTT.Client(pub_clientname)


body_names={}

def parseXML(xml): 
	global body_names
	# create element tree object 
	# tree = ET.parse(xml)

	# get root element 
	#root = tree.getroot()
	root=ET.fromstring(xml)

	body_total=int(root[0][0].text)
	i=1
	while (i<(body_total+1)):
		body_names[i]=str(root[0][i][0].text)
		if (DEBUGGING):
			print("index: "+str(i)+", name: "+str(root[0][i][0].text)+", total: "+str(body_total))
		i+=1
	if (DEBUGGING):
		print(body_names)

def publish_6d(pkt):
	global body_names
	prepend='surf/qtm/'
	[header, bodies] = pkt.get_6d()
	body_count=header[0]
	i=1
	for data in bodies:
		xyz={
			'x':round(data[0][0],2),
			'y':round(data[0][1],2),
			'z':round(data[0][2],2)
		}
		rotation = data[1][0]
		#print(rotation)
		if (not (isnan(xyz['x']) or isnan(xyz['y']) or isnan(xyz['z']))):
			try:
				client.publish(prepend+body_names[i]+'/rotation',json.dumps(rotation))
				client.publish(prepend+body_names[i]+'/position',json.dumps(xyz))
				#print("published: "+prepend+body_names[i])
			except:
				print("failed to publish 6dof:")
				print(i)
				print(body_names[i])
		i+=1

def publish_euler(pkt):
	global body_names
	prepend='surf/qtm/'
	[header,bodies] = pkt.get_6d_euler()
	body_count=header[0]
	i=1
	for data in bodies:
		rph={
			'r':round(data[1][0],2),
			'p':round(data[1][1],2),
			'h':round(data[1][2],2)
		}
		# print(rph)
		if (not (isnan(rph['r']) or isnan(rph['p']) or isnan(rph['h']))):
			try:
				client.publish(prepend+body_names[i]+'/euler',json.dumps(rph))
				print("published: "+prepend+body_names[i])
			except:
				print("failed to publish euler:")
				print(i)
				print(body_names[i])
		i+=1

#function definition
def on_packet(packet):
	""" Callback function that is called everytime a data packet arrives from QTM """
#	print("Framenumber: {}".format(packet.framenumber))
	publish_6d(packet)
	publish_euler(packet)
	


async def setup():
	""" Main function """
	# Connect to MQTT Broker
	try:
			client.connect(mqtt_server)
			print("Connected to MQTT broker: "+mqtt_server)
	except:
			print("didn't connect")

	# Connect to QTM Server
	connection = await qtm.connect(qtm_server)
	if connection is None:
		return

	# Pull Session parameters from QTM, includes rigid body names
	tmp = await connection.get_parameters(parameters=["6d"])

	# saving the xml file (currently the only way I know how to read the incoming packet tmp is to write it to file first)
	# with open('params6D.xml', 'wb') as f: 
		# f.write(tmp)

	# Parse xml file to pull out rigid body names
	# parseXML('params6D.xml')
	parseXML(tmp)
	
	await connection.stream_frames(components=["6d","6dEuler"], on_packet=on_packet)


if __name__ == "__main__":
	asyncio.ensure_future(setup())
	asyncio.get_event_loop().run_forever()


