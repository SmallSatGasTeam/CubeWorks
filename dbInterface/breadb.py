import sys
import sqlite3
import struct
def packetize(isPic, *dataList):
    """
    Takes an list(tuple(data)) from the database and writes a binary stream to a file
    call packetize(*<LIST NAME>, <BOOL VARIABLE>)
    """
    
    if isPic == True:
        ### LOCATE PICTURE FILE AND REPORT THAT TO SHAWN'S PROGRAM
        pass
    elif isPic == False:
        f = open("FILENAME.txt", "a")

        linesTotal = 0

        for tup in dataList:
            for value in tup:
                ba = bytearray(struct.pack("f", value))
                t = ""
                for b in ba:
                    t = "0x%02x" % b
                f.write(t)
                
                #print(t)
            f.write('\n')
            #print('\n')
            linesTotal += 1
    return linesTotal

def getPackets(pacType, numPackets):
    """
    Constructs an sql query based on pacType and numPackets, returns the result.
    """
    lastTransmitted = 0
    connection = sqlite3.connect('../db.sqlite3')
    cursor = connection.execute(f'SELECT * FROM {pacType} WHERE time > {lastTransmitted} ORDER BY time DESC LIMIT {numPackets}')
    rows = cursor.fetchall()
    return rows
    

def getPicture(picNum, res):
    """
    ... Actually, I don't know what this should do yet...
    """
    pass

def getArbitrary(query):
    """
    executes arbitrary sql on the database target, returns whatever comes out.
    """
    connection = sqlite3.connect('../db.sqlite3')
    cursor = connection.execute(query)
    rows = cursor.fetchall()
    return rows


if __name__ == '__main__':
    """
    Usage: command [-flag optional] [options]
    no flag: [<packet_type> <tx_window> <number_of_packets>]
    -a: [<sql_statement>]
    -p: [<picture_number> <resolution>]

    flags: -a, execute arbitrary sql.  Must be followed by a valid sqlite statement.
           -p, get picture.  <picture_number> is a non-negative integer, <resolution> is the size of the picture to prepare.
    """
    data = []
    if sys.argv[1] == '-a':
        data = getArbitrary(sys.argv[2])
    elif sys.argv[1] == '-p':
        data = getPicture(sys.argv[2], sys.argv[3])
    else:
        data = getPackets(sys.argv[1], sys.argv[3])
    print(data)
