import json
from time import sleep
from datetime import datetime
import paho.mqtt.client as MQTT
from gc import collect as trash
import asyncio
import qtm
import xml.etree.ElementTree as ET
from config import *

DEBUGGING=1

client = MQTT.Client("qtm_pub")


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
    while (i<body_total):
        body_names[i]=str(root[0][i][0].text)
        if (DEBUGGING):
            print("index: "+str(i)+", name: "+str(root[0][i][0].text)+", total: "+str(body_total))
        i+=1
    if (DEBUGGING):
        print(body_names)

#function definition
def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    global body_names
#    print("Framenumber: {}".format(packet.framenumber))
    [header, bodies] = packet.get_6d()
    body_count=header[0]
    i=1
    for data in bodies:
        xyz={
            'x':(data[0][0]),
            'y':(data[0][1]),
            'z':(data[0][2])
        }
        rotation = data[1][0]
        #print(rotation)
        try:
            client.publish('qtm/'+body_names[i]+'/rotation',json.dumps(rotation))
            client.publish('qtm/'+body_names[i]+'/position',json.dumps(xyz))
        except:
            pass
        i+=1


async def setup():
    """ Main function """
    # Connect to MQTT Broker
    try:
            client.connect(mqtt_server)
            print("Connected to MQTT broker")
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
    
    await connection.stream_frames(components=["6d"], on_packet=on_packet)


if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()


