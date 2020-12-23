from socket import *
import threading
from queue import Queue
import pickle      #used this for sending object over the connection
from data import * #contains format of message for server and client
import time
from random import *

serverPort = 80
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('0.0.0.0',serverPort))
serverSocket.listen(10)

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue =Queue()
connectedJS = []     #keep track of all connected jobseekers(socket object)
allAddress = []      #keep track of ip address of all job seekers

#to be used for user inputs
IP = ''
Port = 0
hostname = ''

#open file to write output from job seeker
f = open('output.txt', "w")

#to store hops between each client and host
hop = []

signal = ['JOB_SENT']
jobs = ['IS_HOST_ONLINE','PORT_STATUS','TCP_ATTACK','UDP_ATTACK','TRACERT','MAC_IP']


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
            n = int(input("Enter number of jobseekers you want to send job to : "))# all the jobseekers's that server want to send job to
            print('Enter their number:')
            for i in range(0,n):#actual job seeker numbers will be stored in list selectedJS
                selectedJS.append(int(input()))

            if(len(selectedJS)>1):#multiple job seekers
                global hop
                print("What job you want job seeker to perform \n1. IS_HOST_ONLINE \n2. PORT_STATUS\n3.TCP_ATTACK \n4.UDP_ATTACK \n5.TRACERT \n6.MAC_IP\n>>>>" )
                jobNumber=int(input())-1
                user_input(jobNumber)# input required information
                threads = []
                for i in range(0,n):#sending jobs to all job seekers in list using multithreading
                    print(f'<CLIENT {selectedJS[i]}>')
                    msgRecieved = connectedJS[selectedJS[i]-1].recv(1024)
                    data = pickle.loads(msgRecieved)
                    print('****JOB REQUEST FROM CLIENT****')
                    print(data)
                    print('\n')
                    threads.append(threading.Thread(target=processReq,args=(data,selectedJS[i],jobNumber)))
                for i in range(0,n):
                    threads[i].start()
                for i in range(0,n):
                    threads[i].join()

                if(jobNumber==4):
                    closest_hop = 30
                    closest_client_number = ''
                    for h in hop:#comparing no of hops returned by job seekers to check which one is closest to destination
                        if int(h['hops'])<closest_hop:
                            closest_hop = int(h['hops'])
                            closest_client_number = h['jobSeeker']
                    print(f'\nJOB SEEKER #{closest_client_number} IS CLOSEST TO HOST WITH {closest_hop} HOPS ')

            else :#single job seeker
                msgRecieved = connectedJS[selectedJS[i]-1].recv(1024)
                data = pickle.loads(msgRecieved)
                print("What job you want job seeker to perform\n1. IS_HOST_ONLINE \n2. PORT_STATUS\n3.TCP_ATTACK \n4.UDP_ATTACK \n5.TRACERT \n6.MAC_IP\n")
                jobNumber=int(input('>>>>'))-1
                user_input(jobNumber)
                processReq(data,selectedJS[i],jobNumber)#assigning job to job seeker

            for i in range(0,n):#closing and deleting connection to which job is sent.
                selectedJS[i] = selectedJS[i] - i;
                del connectedJS[selectedJS[i]-1]
                del allAddress[selectedJS[i]-1]

            f.close()

def processReq(data,selectedJS,jobNumber):#assigning  job to job seeker
    global hop,f
    if f.closed:
        f = open('output.txt', "a")
    header = data.jobHeader
    if header == 'ASK':
        if(jobNumber == 0):
            x = ServerData(signal[0],jobs[jobNumber],[IP])
        elif(jobNumber == 1 or jobNumber == 2 or jobNumber == 3 ):
            x = ServerData(signal[0],jobs[jobNumber],[IP,Port])
        elif(jobNumber == 4):
            x = ServerData(signal[0],jobs[jobNumber],[hostname])
        elif(jobNumber == 5):
            x = ServerData(signal[0],jobs[jobNumber],[])
        x.msgSize = sys.getsizeof(pickle.dumps(x))
        connectedJS[selectedJS-1].send(pickle.dumps(x))
        result = pickle.loads(connectedJS[selectedJS-1].recv(1024))
        print(f'\n\n****RESULT****')
        result.jobHeader=result.jobHeader+(f'\tClient #{selectedJS}')
        print(result)
        f.write(result.__str__())
        if(jobNumber==4):#adding no of hops between job seeker and host to hop array
            hop.append({'jobSeeker' : selectedJS,'hops':result.jobResult})
        connectedJS[selectedJS-1].close()

def user_input(jobNumber):
    global IP
    global Port
    global hostname
    if(jobNumber == 0):
        print('Please Enter IP:')
        IP = input()
    elif(jobNumber == 1 or jobNumber == 2 or jobNumber == 3 ):
        print('Please Enter IP:')
        IP = input()
        print('Please Enter PortNumber:')
        Port = input()
    elif(jobNumber == 4):
        print('Please Enter hostname:')
        hostname = input()
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
