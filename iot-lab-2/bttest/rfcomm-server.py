import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 8
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print ("Accepted connection from ",address)

data = client_sock.recv(1024)
print ("received [%s]" % data)

client_sock.close()
server_sock.close()