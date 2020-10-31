from socket import *
import pickle
import sys
from data import *


serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.connect(('127.0.0.1',80))

control = ['ASK']
status = ['JOB_COMPLETED']

def response(serverSocket,msgRecv):
    jobType = msgRecv.jobType
    numberOne = msgRecv.jobData[0]
    numberTwo = msgRecv.jobData[1]
    if jobType == 'ADD':
        x = clientData(status[0],str(numberOne+numberTwo))
        x.msgSize = sys.getsizeof(pickle.dumps(x));
        serverSocket.send(pickle.dumps(x))
    elif jobType == 'SUBSTRACT':
        x = clientData(status[0],str(numberOne-numberTwo))
        x.msgSize = sys.getsizeof(pickle.dumps(x));
        serverSocket.send(pickle.dumps(x))
    elif  jobType == 'MULTIPLY':
        x = clientData(status[0],str(numberOne*numberTwo))
        x.msgSize = sys.getsizeof(pickle.dumps(x));
        serverSocket.send(pickle.dumps(x))
    elif jobType == 'DIVIDE':
        x = clientData(status[0],str(numberOne/numberTwo))
        x.msgSize = sys.getsizeof(pickle.dumps(x));
        serverSocket.send(pickle.dumps(x))


x = clientData(control[0],'')
x.msgSize = sys.getsizeof(pickle.dumps(x));
serverSocket.send(pickle.dumps(x))
msgRecv = pickle.loads(serverSocket.recv(1024))
print('****JOB RECEIVED FROM SERVER****')
print(msgRecv)
response(serverSocket,msgRecv)
serverSocket.close()
