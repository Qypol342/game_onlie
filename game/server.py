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
UDPServerSocket.settimeout(3)

#print("UDP server up and listening")
# Listen for incoming datagrams

PLAYER1 = False
PLAYER2 = False
run_ = True
MAX_P = 10

BALLE_VEL = 4
LAST_PING_PLAYER1 =0
LAST_PING_PLAYER2 =0
run = True








def pause():
  global MODE
  global GAMES
  global PLAYER1
  global PLAYER2
  global LAST_PING_PLAYER1

  global run_ 
  run_ =True
  
  if GAMES['PLAYER1'] == {}:
    PLAYER1 = False
  if GAMES['PLAYER2'] == {}:
    PLAYER2 = False
  
  
  
  
  try:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)


    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    #print(PLAYER1,PLAYER2,int(time.time()-LAST_PING_PLAYER1)>0 and PLAYER1 == True,time.time()-LAST_PING_PLAYER1)
    if int(time.time()-LAST_PING_PLAYER1)>1 and PLAYER1 == True:
      print(LAST_PING_PLAYER1,int(time.time()-LAST_PING_PLAYER1))
      
      PLAYER1 = False
      print('player quit 1')

    if eval(message)['type'] == 'IN_GAME_DATA':
      message = str(eval(message)['DATA'])
      if PLAYER1 == False:
        print('player joined 1')
        GAMES['PLAYER1'] ={'Address':address, 'x':eval(message),'SCORE':0}
        LAST_PING_PLAYER1 = time.time() 
        PLAYER1 = True
      elif PLAYER2 == False:
        
        if GAMES['PLAYER1'] != {'Address':address, 'x':eval(message),'SCORE':0}:
          print('player joined 2')
          GAMES['PLAYER2'] ={'Address':address, 'x':eval(message),'SCORE':0}
          PLAYER2 = True
          #print(PLAYER1,PLAYER2)
        else:
          #print('same player', LAST_PING_PLAYER1)
          LAST_PING_PLAYER1 = time.time() 
      else:
        print('full')



      if PLAYER2 == True and PLAYER1 == True:
        GAMES['BALLE'][2] = 2
        MODE = 'RUN'
        threading.Thread(target=balle_sim).start()
    elif eval(message)['type'] == 'SERVER_SEARCH':
      if PLAYER1 == True:
        bytesToSend = str.encode(str({'type':'SERVER_SEARCH_REPOND', 'DATA':'1'}))
        UDPServerSocket.sendto(bytesToSend, address)
      else:
        bytesToSend = str.encode(str({'type':'SERVER_SEARCH_REPOND', 'DATA':'0'}))
        UDPServerSocket.sendto(bytesToSend, address)
  except Exception as e:
    print('no msg recived',e)
  
    


    





def game():

  bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
  message = bytesAddressPair[0]
  address = bytesAddressPair[1]
  global run_
  global GAMES
  global MODE
  global LAST_PING_PLAYER1
  global LAST_PING_PLAYER2


  #print(run_)

  if eval(message)['type'] == 'IN_GAME_DATA':
    message = str(eval(message)['DATA'])

    if address == GAMES['PLAYER1']['Address']:
      GAMES['PLAYER1']['x'] = eval(message)
      LAST_PING_PLAYER1 = time.time()      

      bytesToSend = str.encode(str([GAMES['PLAYER2']['x'],[800 - GAMES['BALLE'][0],  GAMES['BALLE'][1],GAMES['BALLE'][2]],(GAMES['PLAYER1']['SCORE'],GAMES['PLAYER2']['SCORE'])]))
      UDPServerSocket.sendto(bytesToSend, address)

    else:
       GAMES['PLAYER2']['x'] = eval(message)
       LAST_PING_PLAYER2 = time.time()  

       bytesToSend = str.encode(str([GAMES['PLAYER1']['x'],[800 - GAMES['BALLE'][0], 500 - GAMES['BALLE'][1],GAMES['BALLE'][2]],(GAMES['PLAYER2']['SCORE'],GAMES['PLAYER1']['SCORE'])]))
       UDPServerSocket.sendto(bytesToSend, address)
    if run_ == False:
      time.sleep(3)
      MODE = 'PAUSE'
      GAMES['PLAYER1']['SCORE'] = 0 
      GAMES['PLAYER2']['SCORE'] =  0
  elif eval(message)['type'] == 'SERVER_SEARCH':
    bytesToSend = str.encode(str({'type':'SERVER_SEARCH_REPOND', 'DATA':'FULL'}))
    UDPServerSocket.sendto(bytesToSend, address)


    


def balle_sim():
  clock = pygame.time.Clock()
  time.sleep(2)
  global GAMES
  global BALLE_VEL
  global run_
  global MODE
  global PLAYER1
  global PLAYER2
  GAMES['BALLE'][2] = 0
  FPS = 60 
  UP = True
  WIDTH, HEIGHT = 800 , 500 
  r = 20 
  run_ = True
  while run_:
    clock.tick(FPS)
    tt= time.time()
    if int(tt-LAST_PING_PLAYER1)>0 or int(tt-LAST_PING_PLAYER2)>0:
      print(round(tt-LAST_PING_PLAYER1,2),round(tt-LAST_PING_PLAYER2,2))
      run_ = False
      MODE = 'PAUSE'
      if int(tt-LAST_PING_PLAYER1)>0:
        PLAYER2 = False
        GAMES['PLAYER1'] = GAMES['PLAYER2']
      if int(tt-LAST_PING_PLAYER2)>0:
        PLAYER2 = False


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
          #print(tan(distance/60),GAMES['BALLE'][2],BALLE_VEL)
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
        #print('reste1',GAMES['PLAYER1']['SCORE'],GAMES['PLAYER2']['SCORE'])
        time.sleep(1)
    
    else: 
      if GAMES['BALLE'][1]-r<= 50 and GAMES['BALLE'][1]-r> 20:
        iv = 800-GAMES['PLAYER2']['x']
        if GAMES['BALLE'][0]-r <= iv and GAMES['BALLE'][0]+r>= iv-80 : 
          #print('touch2')
          distance = GAMES['BALLE'][0]- (iv- 80//2 )
          
          GAMES['BALLE'][2] = tan(distance/60)*4.5
          
          #BALLE_VEL = 8//GAMES['BALLE'][2]
          #print(tan(distance/60),GAMES['BALLE'][2],BALLE_VEL)
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
        #print('reste2',GAMES['PLAYER1']['SCORE'],GAMES['PLAYER2']['SCORE'])

        time.sleep(1)
  
  print('finishballe_sim')
  

      




GAMES = {"PLAYER1":{}, "PLAYER2":{},"BALLE":[400,250,0]}

MODE ='PAUSE'

def main_server():
  global run 
  while run:
      print(run)


      if MODE == 'PAUSE':
        pause()
      elif MODE == 'RUN':
        game()
def stop_server():
  global run
  run = False
    
if __name__ == "__main__":
  
  main_server()