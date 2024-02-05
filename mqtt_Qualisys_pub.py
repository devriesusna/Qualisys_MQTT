import json
from time import sleep
import paho.mqtt.client as mqtt
import asyncio
import qtm_rt
import xml.etree.ElementTree as ET



pub_topics = ["poseDCM","poseEul"]
strm_qtys = ["6d", "6deuler"]



# Callback function when a connection is established with the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect, return code: ", rc)


def create_body_index(xml_string):
    """ Extract a name to index dictionary from 6dof settings xml """
    xml = ET.fromstring(xml_string)
    body_to_index = {}
    for index, body in enumerate(xml.findall("*/Body/Name")):
        body_to_index[body.text.strip()] = index

    return body_to_index


#function definition
def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """

    #print("Framenumber: {}".format(packet.framenumber))
    if "6d" in strm_qtys:
        #print("6D Packet\n")
        header, bodies = packet.get_6d()
        #print("Component info: {}".format(header))
        for i in range(len(wanted_bodies)):
            if wanted_bodies[i] in body_index:
                msg_DCM = {"name":wanted_bodies[i],"x":bodies[i][0][0],"y":bodies[i][0][1],"z":bodies[i][0][2],"R":bodies[i][1][0]}
                #print(msg_pos)
                client.publish(pub_topics[0],json.dumps(msg_DCM))
                
            
    if "6deuler" in strm_qtys:
        #print('6D Euler Angle Packet')
        header,bodies_euler = packet.get_6d_euler()
        for i in range(len(wanted_bodies)):
            if wanted_bodies[i] in body_index:
                msg_pos = {"name":wanted_bodies[i],"x":bodies_euler[i][0][0],"y":bodies_euler[i][0][1],"z":bodies_euler[i][0][2],"yaw":bodies_euler[i][1][0],"pitch":bodies_euler[i][1][1],"roll":bodies_euler[i][1][2]}
                # print(msg_pos)
                # print(msg_ortn)
                client.publish(pub_topics[1],json.dumps(msg_pos))
                #client.publish(pub_topics[1]+'/'+'orientation',json.dumps(msg_ortn))
            
    
async def setup():
    """ Main function """
    # Connect to MQTT Broker
    global wanted_bodies
    global body_index
    try:
        # Connect to MQTT broker
        client.connect(broker_address, port)
        print("connected to broker")
    except:
        print("didn't connect to broker")

    # Connect to QTM Server
    connection = await qtm_rt.connect("127.0.0.1")
    if connection is None:
        return
    
    # Get 6dof settings from qtm
    xml_string = await connection.get_parameters(parameters=["6d"])
    body_index = create_body_index(xml_string)
    wanted_bodies = list(body_index.keys())
    
    
    await connection.stream_frames(components=strm_qtys, on_packet=on_packet)

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect  # Set the on_connect callback function


# Connect to MQTT broker
broker_address = "10.24.6.23"
port = 1883

body_index = [] # initialize body_index as global variable
wanted_bodies = [] # initializes wanted_bodies as global variable, specify names wanted here

if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()


