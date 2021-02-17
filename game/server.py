import socket
import pygame
import threading
from math import tan
import time
localIP     = "192.168.0.10"
localPort   = 20001
bufferSize  = 1024

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
#UDPServerSocket.settimeout(1)
UDPServerSocket.bind((localIP, localPort))
#print("UDP server up and listening")
# Listen for incoming datagrams

PLAYER1 = False
PLAYER2 = False
run_ = True
MAX_P = 10

BALLE_VEL = 4









def pause():
  global MODE
  global GAMES
  global PLAYER1
  global PLAYER2
  global run_ 
  run_ =True
  
  if GAMES['PLAYER1'] == {}:
    PLAYER1 = False
  if GAMES['PLAYER2'] == {}:
    PLAYER2 = False
  

  bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
  message = bytesAddressPair[0]
  address = bytesAddressPair[1]

  if PLAYER1 == False:
    print('player joined 1')
    GAMES['PLAYER1'] ={'Address':address, 'x':eval(message),'SCORE':0}
    PLAYER1 = True
  elif PLAYER2 == False:
    
    if GAMES['PLAYER1'] != {'Address':address, 'x':eval(message),'SCORE':0}:
      print('player joined 2')
      GAMES['PLAYER2'] ={'Address':address, 'x':eval(message),'SCORE':0}
      PLAYER2 = True
      #print(PLAYER1,PLAYER2)
  else:
    print('full')



  if PLAYER2 == True and PLAYER1 == True:
    GAMES['BALLE'][2] = 2
    MODE = 'RUN'
    threading.Thread(target=balle_sim).start()
    





def run():

  bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
  message = bytesAddressPair[0]
  address = bytesAddressPair[1]
  global run_
  global GAMES
  global MODE

  #print(run_)



  if address == GAMES['PLAYER1']['Address']:
    GAMES['PLAYER1']['x'] = eval(message)
    

    bytesToSend = str.encode(str([GAMES['PLAYER2']['x'],[800 - GAMES['BALLE'][0],  GAMES['BALLE'][1],GAMES['BALLE'][2]],(GAMES['PLAYER1']['SCORE'],GAMES['PLAYER2']['SCORE'])]))
    UDPServerSocket.sendto(bytesToSend, address)

  else:
     GAMES['PLAYER2']['x'] = eval(message)

     bytesToSend = str.encode(str([GAMES['PLAYER1']['x'],[800 - GAMES['BALLE'][0], 500 - GAMES['BALLE'][1],GAMES['BALLE'][2]],(GAMES['PLAYER2']['SCORE'],GAMES['PLAYER1']['SCORE'])]))
     UDPServerSocket.sendto(bytesToSend, address)
  if run_ == False:
    time.sleep(3)
    MODE = 'PAUSE'
    GAMES['PLAYER1']['SCORE'] = 0 
    GAMES['PLAYER2']['SCORE'] =  0
    


def balle_sim():
  clock = pygame.time.Clock()
  time.sleep(2)
  global GAMES
  global BALLE_VEL
  global run_
  GAMES['BALLE'][2] = 0
  FPS = 60 
  UP = True
  WIDTH, HEIGHT = 800 , 500 
  r = 20 
  run_ = True
  while run_:
    clock.tick(FPS)
    #print(GAMES['BALLE'])
    if GAMES['PLAYER1']['SCORE']>= MAX_P or GAMES['PLAYER2']['SCORE']>= MAX_P:
      run_ = False
    if GAMES['BALLE'][0]+r+GAMES['BALLE'][2] > WIDTH:
      GAMES['BALLE'][2] = -GAMES['BALLE'][2]
    elif GAMES['BALLE'][0]-r+GAMES['BALLE'][2] < 0:
      GAMES['BALLE'][2] = -GAMES['BALLE'][2]
    if UP == True :
      #print(GAMES['BALLE'][1]+r> HEIGHT-50)
      iv = 800-GAMES['PLAYER1']['x']
      if GAMES['BALLE'][1]+r>= HEIGHT-50 and GAMES['BALLE'][1]+r< HEIGHT-20:
        
         
        if GAMES['BALLE'][0]-r <= iv and GAMES['BALLE'][0]+r>= iv-80 : 
          print('touch1')
          distance = GAMES['BALLE'][0]- (iv- 80//2 )
          
          GAMES['BALLE'][2] = tan(distance/60)*4
          print(tan(distance/60),GAMES['BALLE'][2],BALLE_VEL)
          #BALLE_VEL = 8//GAMES['BALLE'][2]
          UP = False
          

      




      if GAMES['BALLE'][1]+r < HEIGHT:
        GAMES['BALLE'][1] += BALLE_VEL
        GAMES['BALLE'][0] += GAMES['BALLE'][2]
      else:
        GAMES['BALLE'][0] = 400
        GAMES['BALLE'][1] = 250
        GAMES['BALLE'][2] = 0
        UP = False
        
        GAMES['PLAYER2']['SCORE'] +=1
        print('reste1',GAMES['PLAYER1']['SCORE'],GAMES['PLAYER2']['SCORE'])
        time.sleep(1)
    
    else: 
      if GAMES['BALLE'][1]-r<= 50 and GAMES['BALLE'][1]-r> 20:
        iv = 800-GAMES['PLAYER2']['x']
        if GAMES['BALLE'][0]-r <= iv and GAMES['BALLE'][0]+r>= iv-80 : 
          #print('touch2')
          distance = GAMES['BALLE'][0]- (iv- 80//2 )
          
          GAMES['BALLE'][2] = tan(distance/60)*4.5
          
          #BALLE_VEL = 8//GAMES['BALLE'][2]
          print(tan(distance/60),GAMES['BALLE'][2],BALLE_VEL)
          UP = True
          
          
      if GAMES['BALLE'][1]-r > 0:
        GAMES['BALLE'][1] -= BALLE_VEL
        GAMES['BALLE'][0] += GAMES['BALLE'][2]
      else:
        
        GAMES['BALLE'][0] = 400
        GAMES['BALLE'][1] = 250
        GAMES['BALLE'][2] = 0
        UP = True
        
        GAMES['PLAYER1']['SCORE'] +=1
        print('reste2',GAMES['PLAYER1']['SCORE'],GAMES['PLAYER2']['SCORE'])

        time.sleep(1)
  
  print('finishballe_sim')
  

      




GAMES = {"PLAYER1":{}, "PLAYER2":{},"BALLE":[400,250,0]}

MODE ='PAUSE'



while True:


    if MODE == 'PAUSE':
      pause()
    elif MODE == 'RUN':
      run()
    
