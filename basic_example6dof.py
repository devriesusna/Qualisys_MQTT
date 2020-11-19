"""
    Minimal usage example
    Connects to QTM and streams 3D data forever
    (start QTM first, load file, Play->Play with Real-Time output)
"""

import asyncio
import qtm
import time
import xml.etree.ElementTree as ET

items = []

def parseXML(xmlfile): 
  
    # create element tree object 
    tree = ET.parse(xmlfile)
  
    # get root element 
    root = tree.getroot()
    
    
    # find the names of all the body elements
    for rigbod in root.iter('Name'):
        print(rigbod.text)
        items.append(str(rigbod.text))
    #print(items)
    # TODO: What to do if it returns no rigid bodies


def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    print("Framenumber: {}".format(packet.framenumber))
    header, bodies = packet.get_6d()
    print("Component info: {}".format(header))
    print(items)
    for body in bodies:
        print("\t", body)


async def setup():
    """ Main function """
    connection = await qtm.connect("10.0.0.118")
    if connection is None:
        return
    tmp = await connection.get_parameters(parameters=["6d"])

    # saving the xml file 
    with open('test.xml', 'wb') as f: 
        f.write(tmp)
    
    # Parse xml file to pull out rigid body names
    parseXML('test.xml')
    # Start streaming frames and invoke callback "on_packet" when a frame comes in
    await connection.stream_frames(components=["6d"], on_packet=on_packet)


if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()
