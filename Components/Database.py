from Components.Component import Component
import sqlite3

class Database(Component):
    """
    A database class that implements database creation and methods to read and write from the database.  
    """
    def __init__(self):
        super().__init__("Database", 1)
        self.connection = sqlite3.connect('db.sqlite3')

    def update(self, context):
        """
        Takes a dictionary (context) as a parameter, and writes it to a new row in the database.  
        """
        print(context)
        cursor = self.connection.cursor()
        # TODO: write context to database
        self.connection.commit();

    def initdb(self):
        """
        Creates database tables if they don't exist.
        1. A firstBoot table that stores only the first boot time
        2. A picture table that stores the filepaths of various photos taken
        3. A data table that stores datapoints taken by the sensors
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                CREATE TABLE firstBoot
                (time timestamp PRIMARY KEY) [without rowid]''')
        except:
            pass

        try:
            cursor.execute('''
                CREATE TABLE picture
                (time timestamp PRIMARY KEY,
                filepath text) [without rowid]''')
        except:
            pass

        try:
            cursor.execute('''
                CREATE TABLE data
                (time timestamp PRIMARY KEY,
                uvintensity float,
                boomdeployed bool,
                magx float,
                magy float,
                magz float,
                magxr float,
                magyr float,
                magzr float,
                battvoltage float,
                therm0 float,
                therm1 float,
                therm2 float,
                therm3 float,
                therm4 float,
                therm5 float,
                therm6 float,
                powermode int) [without rowid] ''')

        except:
            pass

        self.connection.commit()
