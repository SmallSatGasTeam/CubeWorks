import sys
import sqlite3
import struct

def packetize(dataList, isPic):
    # dataList = [tup = ()]
	"""
	 Takes an list((tuple(data))) from the database and writes a binary stream to a file
	"""
    if isPic == true:
        ### LOCATE PICTURE FILE AND REPORT THAT TO SHAWN'S PROGRAM
    else:
        f = open("FILENAME.txt", "a")

        linesTotal = 0

        for tup in dataList:
            for value in dataList[tup]:
                ba = bytearray(struct.pack("f", datalist[tup:value]))
                t = ""
                for b in ba:
                    t = "0x%02" % b
                f.write(t)
            f.write('\n')
            linesTotal += 1
    return linesTotal
    pass

def getPackets(pacType, numPackets):
    """
    Constructs an sql query based on pacType and numPackets, returns the result.
    """
    lastTransmitted = 0
    connection = sqlite3.connect('../db.sqlite3')
    cursor = connection.execute(f'select * from {pacType} where time > {lastTransmitted}')
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
    -p: [<picture> <resolution>]
    """
    data = []
    if sys.argv[1] == '-a':
        data = getArbitrary(sys.argv[2])
    elif sys.argv[1] == '-p':
        data = getPicture(sys.argv[2], sys.argv[3])
    else:
        data = getPackets(sys.argv[1], sys.argv[3])
    print(data)
