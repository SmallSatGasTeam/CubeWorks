from Drivers.Driver import Driver

class AntennaDoor(Driver):

    def __init__(self):
        super().__init__("AntennaDoor") #Calls parent constructor

    def readDoorStatus(self):
      #returns the status of all 4 antenna doors
      return (0,0,0,0)

