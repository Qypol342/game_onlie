import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(ip_address)


import subprocess 
  
for ping in range(1,10): 
    address = "192.168.56." + str(ping) 
    res = subprocess.call(['ping', '-c', '3', address]) 
    if res == 0: 
        print( "ping to", address, "OK") 
    elif res == 2: 
    	pass
        #print("no response from", address) 
    else: 
    	pass
        #print("ping to", address, "failed!") 