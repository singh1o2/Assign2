import sys

class clientData:
    def __init__(self,jobHeader,jobResult):
        self.jobHeader = jobHeader
        self.jobResult = jobResult
        self.msgSize = 0
    def __str__(self):
        return f'jobHeader = {self.jobHeader} \n jobResult = {self.jobResult} \n  msgSize = {self.msgSize}'

class ServerData:
    def __init__(self,jobHeader,jobType,jobData):
        self.jobHeader = jobHeader
        self.jobType = jobType
        self.jobData = jobData
        self.msgSize = sys.getsizeof(self)
    def __str__(self):
        return f'jobHeader = {self.jobHeader} \njobType = {self.jobType} \njobData = {self.jobData} \nmsgSize = {self.msgSize}'
