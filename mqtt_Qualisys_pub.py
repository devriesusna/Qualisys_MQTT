import json
from time import sleep
from datetime import datetime
import paho.mqtt.client as MQTT
from gc import collect as trash
import asyncio
import qtm
import xml.etree.ElementTree as ET

client = MQTT.Client("qtm_pub")

pub_topics = [
	'timestamp'
	]

def parseXML(xmlfile): 
    global pub_topics  
    # create element tree object 
    tree = ET.parse(xmlfile)
  
    # get root element 
    root = tree.getroot()
    
    # find the names of all the body elements
    for rigbod in root.iter('Name'):
        print(rigbod.text)
        # append rigid body names to publish topic list
        pub_topics.append(str(rigbod.text))
    #print(items)
    # TODO: What to do if it returns no rigid bodies


#function definition
def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    global pub_topics
    print("Framenumber: {}".format(packet.framenumber))
    [header, bodies] = packet.get_6d()
    print("Component info: {}".format(header))
    print(type(bodies))
    count = 1
    for body in bodies:
        msg = {"x":str(body[0][0]),"y":str(body[0][1]),"z":str(body[0][2])}
        print("\t\n",pub_topics[count],msg,"\t\n")
        client.publish(pub_topics[count],json.dumps(msg))
        count = count+1


async def setup():
    """ Main function """
    # Connect to MQTT Broker
    try:
            client.connect('127.0.0.1')
            print("Connected to MQTT broker")
    except:
            print("didn't connect")

    # Connect to QTM Server
    connection = await qtm.connect("10.0.0.118")
    if connection is None:
        return
    
    # Pull Session parameters from QTM, includes rigid body names
    tmp = await connection.get_parameters(parameters=["6d"])

    # saving the xml file (currently the only way I know how to read the incoming packet tmp is to write it to file first)
    with open('params6D.xml', 'wb') as f: 
        f.write(tmp)
    
    # Parse xml file to pull out rigid body names
    parseXML('params6D.xml')
    
    await connection.stream_frames(components=["6d"], on_packet=on_packet)


if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()


