import os
import sys
sys.path.append('../../')


class FileReset():
    """Checks to ensure that data files exist after reboot. Use "asyncio.run(FileReset.fullReset())" to run.
    
    Includes program to manually reset individual files for testing purposes. Use "asyncio.run(FileReset.fullReset())" to run."""
    def __init__(self):
        # List of file paths
        self.__FILE_PATHS = [ 
            "../TXISR/data/flagsFile.txt" , 
            "../TXISR/data/txFile.txt" , 
            "../TXISR/data/txWindows.txt" , 
            "../TXISR/data/transmissionFlag.txt" , 
            "../TXISR/data/AX25Flag.txt",
            "../flightLogic/backupBootRecords.txt" , 
            "../flightLogic/bootRecords.txt" , 
            "../flightLogic/data/Attitude_Data.txt" , 
            "../flightLogic/data/Deploy_Data.txt" , 
            "../flightLogic/data/TTNC_Data.txt" ]
        self.__filePath = ""
        self.fullReset()

    def __reset(self):
        """Opens and erases file, certain files are then filled with required text. If there is no file under a certain file path, it will create the file."""
        # Depending on the file path, replaces the empty file with a string of text based on what data will be written in the file
        try:
            file = open(self.__filePath, 'w')
        except:
            # Check the dir
            self.dirProtection()
            # If the file doesn't exist it creates a new one
            file = open(self.__filePath, 'w+')
            
        if self.__filePath == "../flightLogic/backupBootRecords.txt" or self.__filePath == "../flightLogic/bootRecords.txt" or self.__filePath == "../bootRecords.txt":
            file.write("0\n0\n0\n")
            file.close()
        if self.__filePath == "../TXISR/data/flagsFile.txt" or self.__filePath == "../flagsFile.txt":
            file.write("0\n0\n0\n0\n0\n")
            file.close()
        if self.__filePath == "../TXISR/data/transmissionFlag.txt" or self.__filePath == "../transmissionFlag.txt":
            file.write("Enabled")
            file.close()
        if self.__filePath == "../TXISR/data/AX25Flag.txt" or self.__filePath == "../AX25Flag.txt":
            file.write("Disabled")
            file.close()
        # This closes the file so it is no longer being edited
    
    def fullReset(self):
        """Checks to make sure that files necessary for reboot exist, if they don't, it creates them."""
        # Runs through every file in FILE_PATHS list
        for i in self.__FILE_PATHS:
            # Opens the file to see if it exists
            try:
                file = open(i)
                print("File being checked " + i)
            # If it doesn't, it runs reset to create it
            except OSError:
                print("File being reset" + i)
                self.__filePath = i
                self.__reset()
            # Otherwise it just closes the file
            else:
                file.close()

    def individualReset(self, newFile):
        self.__filePath = newFile
        """Allows the manual reset of a single file."""
        # Runs reset once for a single file
        self.__reset()
        print("File being reset " + self.__filePath)

    # This check a single file to see if it will open or not if not it resets it 
    def checkFile(self, newFile):
        self.__filePath = newFile
        
        self.dirProtection()

        try:
            file = open(self.__filePath)
        except OSError:
            self.__reset()
            print("File being reset " + self.__filePath)
        else:
            file.close()
            print("File is ok " + self.__filePath)

    # This checks a single directory to see if it exists
    def checkDir(self, path):
        isdir = os.path.isdir(path)    
        return isdir

    # This makes the diretory if it files
    def dirProtection(self):  
        count = 0
        # Find the directory path
        for i in range(len(self.__filePath)):
            if self.__filePath[-i] == "/":
                break
            count += 1
        dirPath = self.__filePath[:len(self.__filePath) - count]
        
        # Check directory
        # The dir doesnt exist recreate it
        if(not self.checkDir(dirPath)):
            try:
                os.mkdir(dirPath)
            except:
                print("Error trying to make directory ", dirPath)