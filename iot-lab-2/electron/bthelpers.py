import bluetooth
import json

target_name = "raspberrypi"
sock = None

# TODO: Implement server for p2p comms

def start_client():    
    target_address = None
    nearby_devices = bluetooth.discover_devices()

    for bdaddr in nearby_devices:
        print(bluetooth.lookup_name( bdaddr ))
        if target_name == bluetooth.lookup_name( bdaddr ):
            target_address = bdaddr
            break

    if target_address is not None:
        print ("found target bluetooth device with address ", target_address)
    else:
        print ("could not find target bluetooth device nearby")

    port = 1

    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((target_address, port))      

def set_target(target):
    target_name = target

def send_data(data):
    sock.send(json.dumps(data))

def terminate():
    sock.close()


