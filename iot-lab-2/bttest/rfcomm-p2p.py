import bluetooth
import threading

client_sock = None
server_sock = None
sock = None
target_name = "raspberrypi"

def start_server():
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)

    client_sock,address = server_sock.accept()
    print ("Accepted connection from ",address)

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


'''
sth = threading.Thread(target=start_server)
cth = threading.Thread(target=start_client)

sth.start()
cth.start()

cth.join()
sth.join()
'''

#start_client()
start_server()

i = 0
try:
    while True:
        tosend = "Sent to" + target_name +  str(i)
        sock.send(tosend)     

        data = client_sock.recv(1024)
        if not data:
            break
        print("Received from " + target_name, data, " ", str(i))
        i+=1
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
sock.close()
print("All done.")



