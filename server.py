import socket              
import pickle
import numpy
import paramiko
from paramiko import SSHClient



file_name='s01.dat'
with open(file_name, 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    loaded_data = u.load()
data=loaded_data['data']

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.104',username='root',password='toortoor')

stdin , stdout ,stderr = client.exec_command('python3.7 client.py')
# print(stdout.read().decode('utf8'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.102',778))
s.listen(1)


clientsocket, address = s.accept()
print(address)


for i in range(8064):
    print(i)
    for j in range(32):
        num=data[0][j][i]
        v=bin(int(num/0.0001695752)).split('b')[1]
        v='0'*(24-len(v))+v

        clientsocket.send(bytes([int(v[-8:],2)]))
        clientsocket.send(bytes([int(v[-16:-8],2)]))
        clientsocket.send(bytes([int(v[-24:-16],2)]))

s.close()


