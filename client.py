import numpy                     
import socket
  
import threading
import time

import tensorflow as tf

# TCP/IP setup
TCP_IP = '192.168.1.102' 
TCP_PORT = 778     
BUFFER_SIZE = 1536
 
# Open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
 


import LPi.GPIO as GPIO
GPIO.setmode (GPIO.BOARD)
GPIO.setup (2, GPIO.OUT)


signal_buffer = numpy.zeros((32,16))
data_array=numpy.zeros((32,0))

model= tf.keras.models.load_model('model.h5')

def thread_function():

    index=0
    while(True):

        if data_array.shape[1] >= (index+2)*384:
            data = data_array[:,384*(index+1) :384*(index+2)]-data_array[:,:384]
            result=model.predict(data.reshape(1,32,384))

            result = result.argmax(axis = -1)

            GPIO.output(2, result[0])

            index+=1
            print(data.shape)

x = threading.Thread(target=thread_function)
x.start() 

while(True):
    data = []
    while len(data) != BUFFER_SIZE:
        data += s.recv(BUFFER_SIZE)
    for m in range(16):
        for i in range(32):
            
        
            offset = m * 3 * 32 + i*3
            # The 3 bytes of each sample arrive in reverse order
            sample = ((data[offset+2]) << 16)
            sample += ((data[offset+1]) << 8)
            sample += (data[offset])
            # Store sample to signal buffer
            signal_buffer[i,m] = sample * 0.0001695752
    
    data_array=numpy.concatenate((data_array,signal_buffer),axis=1)
    print(data_array.shape)



print(data_array.shape)
s.close()