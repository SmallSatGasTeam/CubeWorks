# importing "heapq" to implement heap queue
from protectionProticol.fileProtection import FileReset

""" This checks the contents of the txWindows.txt and grabs the shortest time stamp to transmit first. """

class Queue ():
    def __init__(self, filepath):
        print("Making the queue")
        self.__filepath = filepath
        self.__fileChecher = FileReset()

    def enqueue(self, data):
        self.__fileChecher.checkFile(self.__filepath)
        file = open(self.__filepath, "a+") 
        file.write(str(data) + "\n")
        file.close()

    def dequeue(self, delet):
        return self.__short(delet)


    def __short(self, delete):
        contents = []
        line = []
        minLine = ""
        self.__fileChecher.checkFile(self.__filepath)
        file = open(self.__filepath, "r") 
        contents = file.read().splitlines()
        file.close()
        #print("Printing contents", contents)
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
                if(int(line[0]) >= 0):
                    file.write(j + "\n")
            file.close()
        if(not delete):
            return int (min[0])
        else :
            return minLine

    def clearQueue(self):
        self.__fileChecher.checkFile(self.__filepath)
        file = open(self.__filepath, "w")
        file.close()


#this is for testing
# def main():
#     test = Queue("temp.txt")
#     test.enqueue("5,0,0,00000000")
#     test.enqueue("4,0,0,00000000")
#     test.enqueue("3,0,0,00000000")
#     test.enqueue("2,0,0,00000000")
#     test.enqueue("-1,0,0,00000000")

#     #test.clearQueue()
#     print(test.dequeue(True))
#     print(test.dequeue(True))
#     print(test.dequeue(False))
#     print(test.dequeue(False))

# main()