# OSC Server Code from ChatGPT
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
import json
import matplotlib.pyplot as plt
from four_part_helper import *
import numpy as np
import random

random.seed(3)

# this client will send back to Sonic Pi on its default OSC-in port 4560
reply_client = SimpleUDPClient("127.0.0.1", 4560)

# Default Chords: I IV V 1
C = np.matrix([
      [0,4,7],
      [5,9,0],
      [7,11,2],
      [0,4,7]
])
C = C.T
X = np.matrix([[random.randint(36,88) for j in range(C.shape[1])] for i in range(4)])



def handle_request(address, *args):
    global X
    global C
    global chord_sum_means
    if args:
      json_str, inc = args
      increment = inc
      C = json.loads(json_str)
      C = np.matrix(C)
      C = C.T
      print(C)
      C = C % 12
      
      if C.shape[1] != X.shape[1]:
         X = np.matrix([[random.randint(0,88) for j in range(C.shape[1])] for i in range(4)])
      print(X)
         
    print(increment)
    chord_sums = []
    continu_sums = []
    for _ in range(increment):
      X, chord_sum, continu_sum = update(X, C, chord_sim_strength=4.75, continu_strength=0.025)
      chord_sums.append(chord_sum)
      continu_sums.append(continu_sum)
    
    notes_2d = X.tolist()  
    flat = [n for row in notes_2d for n in row]
    reply_client.send_message("/python_reply", flat)
    print(X)
    print(chord_similarity(X, C))


disp = Dispatcher()
disp.map("/py_request", handle_request)

server = BlockingOSCUDPServer(("127.0.0.1", 4559), disp)
print("Python OSC server listening on port 4559…")
server.serve_forever()
