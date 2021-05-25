# importing "heapq" to implement heap queue
#from protectionProticol.fileProtection import FileReset

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

    def dequeue(self):
        return self.__short()


    def incramentTime(self):
        contents = []
        self.__fileChecher.checkFile(self.__filepath)
        file = open(self.__filepath, "r") 
        contents = file.read().splitlines()
        file.close()
        for i in range (len(contents)):
            contents[i] = str(int (contents[i]) - 1)
        file = open(self.__filepath, "w")
        for i in contents:
            file.write(i + "\n")
        file.close()


    def __short(self):
        contents = []
        self.__fileChecher.checkFile(self.__filepath)
        file = open(self.__filepath, "r") 
        contents = file.read().splitlines()
        file.close()
        print(contents)
        if(len(contents) == 0):
            return None
        if(contents[0] != -1 ):
            min = int (contents[0])
            for i in contents:
                if(int(i) < min and int(i) >= 0): 
                    min = int(i)
            contents.remove(str (min))
            file = open(self.__filepath, "w") 
            for j in contents:
                if(int(j) >= 0):
                    file.write(j + "\n")
            file.close()
        return min

    def clearQueue(self):
        file = open(self.__filepath, "w")
        file.close()

#this is for testing
# def main():
#     test = Queue("temp.txt")
#     test.enqueue(5)
#     test.enqueue(4)
#     test.enqueue(2)
#     test.enqueue(3)
#     test.enqueue(0)
#     test.enqueue(-1)

#     #test.clearQueue()

#     test.incramentTime()
#     print(test.dequeue())
#     test.incramentTime()
#     print(test.dequeue())
#     test.incramentTime()
#     print(test.dequeue())
#     test.incramentTime()
#     print(test.dequeue())
#     test.incramentTime()

# main()