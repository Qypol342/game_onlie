import socket
import pygame
import threading
localIP     = "192.168.0.10"
localPort   = 20001
bufferSize  = 1024

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
#UDPServerSocket.settimeout(1)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
# Listen for incoming datagrams

PLAYER1 = False
PLAYER2 = False











def pause():
  global MODE
  global GAMES
  global PLAYER1
  global PLAYER2
  if GAMES['PLAYER1'] == {}:
    PLAYER1 = False
  if GAMES['PLAYER2'] == {}:
    PLAYER2 = False
  

  bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
  message = bytesAddressPair[0]
  address = bytesAddressPair[1]

  if PLAYER1 == False:
    print('player joined 1')
    GAMES['PLAYER1'] ={'Address':address, 'x':eval(message)}
    PLAYER1 = True
  elif PLAYER2 == False:
    
    if GAMES['PLAYER1'] != {'Address':address, 'x':eval(message)}:
      print('player joined 2')
      GAMES['PLAYER2'] ={'Address':address, 'x':eval(message)}
      PLAYER2 = True
      print(PLAYER1,PLAYER2)
  else:
    print('full')



  if PLAYER2 == True and PLAYER1 == True:
    GAMES['BALLE'][2] = 1
    MODE = 'RUN'
    threading.Thread(target=balle_sim).start()




def run():
  #print(GAMES)
  bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
  message = bytesAddressPair[0]
  address = bytesAddressPair[1]

  if address == GAMES['PLAYER1']['Address']:
    GAMES['PLAYER1']['x'] = eval(message)

    bytesToSend = str.encode(str([GAMES['PLAYER2']['x'],GAMES['BALLE']]))
    UDPServerSocket.sendto(bytesToSend, address)

  else:
     GAMES['PLAYER2']['x'] = eval(message)

     bytesToSend = str.encode(str([GAMES['PLAYER1']['x'],GAMES['BALLE']]))
     UDPServerSocket.sendto(bytesToSend, address)

def balle_sim():
  clock = pygame.time.Clock()
  global GAMES
  FPS = 60 
  while run:
    clock.tick(FPS)
    print(GAMES['BALLE'])

    if GAMES['BALLE'][2] != 0:
      if GAMES['BALLE'][0] <= 20:
        GAMES['BALLE'][2] = -GAMES['BALLE'][2]
      if GAMES['BALLE'][0] >= 800- 20:
        GAMES['BALLE'][2] = -GAMES['BALLE'][2]
      GAMES['BALLE'][1] -= 1
      GAMES['BALLE'][0] += GAMES['BALLE'][2]
    if GAMES['BALLE'][1]+20 >= 450:
    
      if GAMES['BALLE'][0]+20 > GAMES['PLAYER1'] and GAMES['BALLE'][0]-20< GAMES['PLAYER1']+80 :
        print('touch')
        distance = GAMES['BALLE'][0] - GAMES['PLAYER1'] - 80//2 
        print(tan(distance/60))
        GAMES['BALLE'][2] = tan(distance/60)



GAMES = {"PLAYER1":{}, "PLAYER2":{},"BALLE":[400,200,0]}

MODE ='PAUSE'



while True:

    #print(MODE)
    if MODE == 'PAUSE':
      pause()
    elif MODE == 'RUN':
      run()
    






'''
import socket
localIP     = "192.168.0.10"
localPort   = 20001
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
# Listen for incoming datagrams

GAMES={1212:{'GAME_ID': 1212,'PLAYER':{}, 'BALLE':{'X':400,'Y':400,'V':0}}}

def IN_GAME_DATA(ms):
  #global address
  global GAMES

  gm = None
  if  ms['DATA']['GAME_ID'] in GAMES:
      gm = GAMES[ms['DATA']['GAME_ID']]
  print('gm',gm)
  if gm == None:
    GAMES.append({'GAME_ID': ms['DATA']['GAME_ID'],'PLAYER':{}, 'BALLE':{'X':400,'Y':400,'V':0}})
  if len(gm['PLAYER']) == 0:
    gm['PLAYER'].update( {address:{'PADDLE':ms['DATA']['PADDEL']}})
  elif len(gm['PLAYER']) == 1:
    gm['PLAYER'].update( {address:{'PADDLE':ms['DATA']['PADDEL']}})




while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    ms  = eval(message)
    sorte = ms['type']
    if sorte == 'IN_GAME_DATA':
      IN_GAME_DATA(ms)
    elif sorte == 'IN_GAME_DATA_REQUEST':
      for i in GAMES:
        if i == ms['DATA']['GAME_ID']:
          if len(GAMES[i]['PLAYER']) == 2:
          msgFromServer       = str({'type':'IN_GAME_DATA_REQUEST_RESULT','DATA':{'BALLE':GAMES[i]['BALLE']}})
          bytesToSend         = str.encode(msgFromServer)
          UDPServerSocket.sendto(bytesToSend, address)
          break

     
    print(clientIP)

   

    # Sending a reply to client
    if eval(message)['type'] == 'server_recherche':
      msgFromServer       = "{'type':server_found}"

    else:

      msgFromServer       = "{'type':'Hello UDP Client'}"


    bytesToSend         = str.encode(msgFromServer)

    UDPServerSocket.sendto(bytesToSend, address)


    '''