import time 
import threading
x =2
def run():
	global x
	while True:
		print(x)
		time.sleep(2)
threading.Thread(target=run).start()
	
x =23 
time.sleep(2)
x =23456 
time.sleep(2)
x =23451111111
time.sleep(2)
x =2345444
time.sleep(2)