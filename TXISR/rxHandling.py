import io
import Check
import breadb


class TXISR:
    '''
    TODO:
        interrupt
    '''

    '''
    rxData holds the values gotten from the grounds transmission. (see Flight Logic doc appendix c table 5)
    0 = packet type
    1 = window start
    2 = window duration
    3 = data type
    4 = picture number (if applicable)
    '''
    rxData = []

    def __init__(self):
        self.TX = io.open("/dev/tty/AMA0", 'r')
        self.readTX()

        # not sure what im getting back
        # self.sendTosrCheck()

    def interrupt(self):
        pass

    def readTX(self):
        for i in range(5):
            currentData = self.TX.readline()
            currentData = self.decodeTX(currentData)
            self.rxData.append(currentData)

    def decodeTX(self, hexMessage):
        return bytes.fromhex(hexMessage).decode('utf-8')

    def sendTosrCheck(self):
        Check(self.rxData[3], self.rxData[1], self.rxData[2])

    def sendTobreadb(self):
        if self.rxData[4].compareTo(None):
            breadb.driveDataType(self.rxData[0], self.rxData[1], self.rxData[2], self.rxData[3])
        else:
            breadb.drivePic(self.rxData[0], self.rxData[1], self.rxData[2], self.rxData[3], self.rxData[4])

