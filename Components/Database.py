from Components.Component import Component
import sqlite3
from datetime import datetime

class Database(Component):
    """
    A database class that implements database creation and methods to read and write from the database. Creates the following tables: 
    1. firstBoot
    2. picture
    3. attitudeDetermination
    4. data
    5. housekeeping
    """
    def __init__(self):
        """
        Initializes a Database object, calls the parent constructor, and connects to a sqlite3 database.
        """
        super().__init__("Database", 1)
        self.connection = sqlite3.connect('db.sqlite3')
        self.initdb()

    def update(self, context):
        """
        Concrete implementation of Component.update().
        Takes a dictionary (context) as a parameter, and writes it to a new row in the database.  
        """
        print('writing to database')
        self.commitPicture(context)
        self.commitTTNC(context)
        self.commitBoomDeploy(context)
        self.commitAttitude(context)
        #cursor = self.connection.cursor()
        # TODO: write context to database
        #self.connection.commit()


    def getFirstBoot(self):
        """
        Queries the firstBoot table in the database and returns the firstBoot value if it exists.
        If no firstBoot value exists, returns None.
        """
        cursor = self.connection.execute("SELECT * FROM first_boot")
        rows = cursor.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][0]


    def setFirstBoot(self, time):
        """
        Takes a datetime string as a parameter and inserts
        it into the firstBoot table in the database.  
        """
        insertCommand = """INSERT INTO firstBoot VALUES (?);"""
        self.connection.execute("INSERT INTO first_boot VALUES(?)", (time,))
        self.connection.commit()


    def commitPicture(self, context):
        """
        Parses context and commits relevant picture data to db.
        1. check for all relevant keys in context
        2. if key exists, put it in the pre-commit data string
        3. else, put a default value in the string
        4. commit string
        """
        print('commit picture data')


    def commitTTNC(self, context):
        """
        Parses context and commits relevant TT&C data to db.
        """
        print('commit TT&C data')
    
    def commitBoomDeploy(self, context):
        """
        Parses context and commits relevant boom deployment data to db.
        """
        print('commit boom deploy data')
        self.connection.execute("INSERT INTO boom_deploy (time, packet_type, boombox_uv, la_x, la_y, la_z) VALUES (?, ?, ?, ?, ?, ?)", (context['rtc'], 0, 0.0, 0.0, 0.0, 0.0))
        self.connection.commit()


    def commitAttitude(self, context):
        """
        Parses context and commits relevant attatude data to db.
        """
        print('commit attitude data')


    def initdb(self):
        """
        Creates database tables if they don't exist.
        1. A firstBoot table that stores only the first boot time
        2. A picture table that stores the filepaths of various photos taken
        3. A data table that stores datapoints taken by the sensors
        Note that the "+" and "-" characters will cause SQLite to emit a syntax error if 
        put in a column name
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS first_boot
            (time int PRIMARY KEY)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS picture
            (time int PRIMARY KEY,
            text path,
            int packetNum,
            blob packet)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ttnc
            (time int PRIMARY KEY,
            packet_type int,
            mission_mode int,
            reboot_count int,
            boombox_uv float,
            sp_x_pos_temp0 float,
            sp_z_pos_temp1 float,
            raspi_temp float,
            eps_mcu_temp float,
            batt_temp_cell0 float,
            batt_temp_cell1 float,
            batt_temp_cell2 float,
            batt_temp_cell3 float,
            batt_voltage float,
            batt_current float,
            bcr_voltage float,
            bcr_current float,
            eps_3v3_current float,
            eps_5v current float,
            sp_x_voltage float,
            sp_x_pos_current float,
            sp_x_neg_current float,
            sp_y_voltage float,
            sp_y_pos_current float,
            sp_y_neg_current float,
            sp_z_voltage float)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS boom_deploy
            (time int PRIMARY KEY,
            packet_type int,
            boombox_uv float,
            la_x float,
            la_y float,
            la_z float)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attitude
            (time int PRIMARY KEY,
            packet_type float,
            ss_0 float,
            ss_1 float,
            ss_2 float,
            ss_3 float,
            ss_4 float,
            mf_x float,
            mf_y float,
            mf_z float)''')

        self.connection.commit()
