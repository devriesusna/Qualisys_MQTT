import json
from time import sleep
from datetime import datetime
import paho.mqtt.client as MQTT
from gc import collect as trash
import asyncio
import qtm

client = MQTT.Client("qtm_pub")

pub_topics = {
	'timestamp',
	'bodyA',
        'bodyB',
        'bodyC',
        'bodyD'
}

example_dict = {
	'x':'0',
	'y':'1',
	'z':'2'
}
#function definition
def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    global pub_topics
    print("Framenumber: {}".format(packet.framenumber))
    [header, bodies] = packet.get_6d()
    print("Component info: {}".format(header))
    print(type(bodies))
    print("break","\t")
    for body in bodies:
        tmp = {"x":str(body[0][0]),"y":str(body[0][1]),"z":str(body[0][2])}
        print("\t\n",body[0][0],"\t\n")
        print(body[1])
        print("\t\n","break")
        client.publish('bodyA',json.dumps(tmp))
#        client.publish('x_position',str(body[0][0]))
 #       client.publish('y_position',str(body[0][1]))
  #      client.publish('z_position',str(body[0][2]))



async def setup():
    """ Main function """
    try:
            client.connect('127.0.0.1')
            print("Connected to MQTT broker")
    except:
            print("didn't connect")
    connection = await qtm.connect("10.0.0.118")
    if connection is None:
        return

    await connection.get_parameters(parameters=["6d"])
    
    await connection.stream_frames(components=["6d"], on_packet=on_packet)


if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()


