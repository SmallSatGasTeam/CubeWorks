# importing "heapq" to implement heap queue
#from protectionProticol.fileProtection import FileReset

class Queue ():
    def __init__(self, filepath):
        print("Making the queue")
        self.__filepath = filepath
        #self.__fileChecher = FileReset()

    def enqueue(self, data):
        #self.__fileChecher.checkFile(self.__filepath)
        file = open(self.__filepath, "a+") 
        file.write(str(data) + "\n")
        file.close()

    def dequeue(self):
        return self.__short()

    def incramentTime(self):
        pass

    def __short(self):
        contents = []
        #self.__fileChecher.checkFile(self.__filepath)
        file = open(self.__filepath, "r")
        contents = file.read().splitlines()
        file.close()
        print(contents)
        if(int(contents[0]) != -1 ):
            min = int (contents[0])
            for i in contents:
                if(int(i) < min) and (int(i) != -1): 
                    min = int(i)
            contents.remove(str (min))
            file = open(self.__filepath, "w") 
            for j in contents:
                file.write(j + "\n")
            file.close()
        return min

#this is for testing
# def main():
#     test = Queue("temp.txt")
#     test.enqueue(5)
#     test.enqueue(4)
#     test.enqueue(2)
#     test.enqueue(3)

#     print(test.dequeue())
#     print(test.dequeue())
#     print(test.dequeue())
#     print(test.dequeue())

# main()