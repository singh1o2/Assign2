from socket import *
import threading
from queue import Queue
import pickle      #used this for sending object over the connection
from data import * #contains format of message for server and client
import time
from random import *

serverPort = 80
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(10)

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue =Queue()
connectedJS = []     #keep track of all connected jobseekers(socket object)
allAddress = []      #keep track of ip address of all job seekers

signal = ['JOB_SENT']
jobs = ['ADD','SUBSTRACT','MULTIPLY','DIVIDE']


def acceptConnections():
    for x in connectedJS: #closing previous connection
        x.close()

    del connectedJS[:] #freeing any previoud data(connections) stored in two lists
    del allAddress[:]

    while True:
        print('..................Waiting for new client ................')
        clientSocket,address = serverSocket.accept()
        connectedJS.append(clientSocket)
        allAddress.append(address)
        print(f'\nConnection established at {address}')

def sendJobs():
        while True:
            if len(connectedJS)<=0: #initially there will not be any connection so we cannot proceed further
               time.sleep(2)
               continue
            while True:
                print('Available Job seekers are:')
                index = 0
                for x in allAddress: #print all jobseekers
                     index+=1
                     print(f'{index}   {x}')
                print('Checking if more client connects in next 5 seconds...\n')
                time.sleep(5)
                if len(allAddress)>(index):
                    continue;
                else:
                    break;

            print('Proceeding with Available clients...')
            print('New clients will have to wait for job.....')


            selectedJS =[]
            n = int(input("Enter number of jobseekers you want to send job to : "))# all the js's that server want to send job to
            print('Enter their number:')
            for i in range(0,n):#actual job seeker numbers will be stored in list selectedJS
                selectedJS.append(int(input()))

            for i in range(0,n):#sending jobs to all job seekers in list
                print(f'<CLIENT {i+1}>')
                msgRecieved = connectedJS[selectedJS[i]-1].recv(1024)
                data = pickle.loads(msgRecieved)
                print('****JOB REQUEST FROM CLIENT****')
                print(data)
                print('\n')
                processReq(data,selectedJS[i])#assigning random job to job seeker

            for i in range(0,n):#closing and deleting connection to which job is sent.
                selectedJS[i] = selectedJS[i] - i;
                del connectedJS[selectedJS[i]-1]
                del allAddress[selectedJS[i]-1]

def processReq(data,selectedJS):#assigning random job to job seeker
    header = data.jobHeader
    if header == 'ASK':
        seed(time.time())
        x = ServerData(signal[0],jobs[randint(0, 3)],[randint(0, 20000),randint(1, 20000)])
        x.msgSize = sys.getsizeof(pickle.dumps(x));
        connectedJS[selectedJS-1].send(pickle.dumps(x))
        result = pickle.loads(connectedJS[selectedJS-1].recv(1024))
        print('****RESULT FROM CLIENT****')
        print(result)
        print('\n')
        connectedJS[selectedJS-1].close()

#multi threading for handling connections as well as sending data to connections simultaneously
def createThreads():
    for a in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon =True #free resources
        t.start()

def createJobs():
    for a in JOB_NUMBER:
        queue.put(a)
    queue.join()

def work():
    while True:
        x  = queue.get()
        if x==1:
            acceptConnections()
        if x==2:
            sendJobs()
        queue.task_done()


createThreads()
createJobs()
