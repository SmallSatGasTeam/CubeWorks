# importing "heapq" to implement heap queue
from protectionProticol.fileProtection import FileReset

""" This checks the contents of the txWindows.txt and grabs the shortest time stamp to transmit first. """

class Queue():
    def __init__(self, filepath):
        print("Making the queue")
        self.__filepath = filepath
        self.__fileChecher = FileReset()

    #this adds a data point to the txWindows folder
    def enqueue(self, data):
        self.__fileChecher.checkFile(self.__filepath)
        self.__fileChecher.windowProtection()
        file = open(self.__filepath, "a+") 
        file.write(str(data) + "\n")
        file.close()

    
    #this code returns data form the queue, if you say true it will return the whole line and delete that line from the queue. If you give it a 1 then it returns the next time but 
    #does not delete the data in the queue
    def dequeue(self, delet):
        self.__fileChecher.checkFile(self.__filepath)
        self.__fileChecher.windowProtection()
        return self.__short(delet)


    #this function returns the next time that is stored in the file. If you give it a true it returns the all the data that is stored in the file, and then deletes the line. 
    #if it is given a 0 then it will just return the time to the next window. 
    def __short(self, delete):
        #print("starting short")
        contents = []
        line = []
        minLine = ""
        self.__fileChecher.checkFile(self.__filepath)
        self.__fileChecher.windowProtection()
        file = open(self.__filepath, "r") 
        contents = file.read().splitlines()
        file.close()
        if(len(contents) == 0):
            return -1
        line = contents[0].split(',')
        if(line[0] != -1 ):
            min = line
            minLine = contents[0]
            for i in contents:
                line = i.split(',')
                if line[0] != '':
                    if(int(line[0]) < int(min[0]) and int(line[0]) >= 0): 
                        min = line
                        minLine = i
            contents.remove(minLine)
            self.__fileChecher.checkFile(self.__filepath)
            file = open(self.__filepath, "w")
            if(not delete):
                file.write(minLine + "\n")
            for j in contents:
                line = j.split(',')
                if line[0] != '':
                    if(int(line[0]) >= 0):
                        file.write(j + "\n")
            file.close()
        if(not delete):
            return int (min[0])
        else :
            return minLine

    def clearQueue(self):
        self.__fileChecher.checkFile(self.__filepath)
        self.__fileChecher.windowProtection()
        file = open(self.__filepath, "w")
        file.close()