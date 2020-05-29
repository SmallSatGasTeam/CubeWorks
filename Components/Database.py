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
        #cursor = self.connection.cursor()
        # TODO: write context to database
        #self.connection.commit()


    def getFirstBoot(self):
        """
        Querys the firstBoot table in the database and returns the firstBoot value if it exists.
        If no firstBoot value exists, returns None.
        """
        cursor = self.connection.execute("SELECT * FROM firstBoot")
        rows = cursor.fetchall()
        if len(rows) == 0:
            return None
        return datetime.strptime(rows[0][0], '%Y-%m-%d %H:%M:%S.%f')


    def setFirstBoot(self, time):
        """
        Takes a datetime string as a parameter and inserts
        it into the firstBoot table in the database.  
        """
        insertCommand = """INSERT INTO firstBoot VALUES (?);"""
        self.connection.execute("INSERT INTO firstBoot VALUES(?)", (time,))
        self.connection.commit()


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
            CREATE TABLE IF NOT EXISTS firstBoot
            (time timestamp PRIMARY KEY)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS picture
            (time timestamp PRIMARY KEY,
            packet_type int,
            mission_mode int,
            reboot_count int,
            payload_size int,
            payload_count int,
            filepath text)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attitudeDetermination
            (time timestamp PRIMARY KEY,
            packet_type int,
            mission_mode int,
            reboot_count int,
            payload_size int,
            payload_count int,
            ss_1 float,
            ss_2 float,
            ss_3 float,
            ss_4 float,
            ss_5 float,
            mf_x float,
            mf_y float,
            mf_z float,
            la_x float,
            la_y float,
            la_z float,
            powermode int)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data
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
            powermode int)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS housekeeping
            (time timestamp PRIMARY KEY,
            packet_type int,
            mission_mode int,
            reboot_count int,
            payload_size int,
            payload_count int,
            boombox_uv float,
            raspi_temp float,
            eps_mcu_temp float,
            batt_temp_cell_1 float,
            batt_temp_cell_2 float,
            batt_temp_cell_3 float,
            batt_temp_cell_4 float,
            batt_voltage float,
            batt_current float,
            bcr_voltage float,
            bcr_current float,
            eps_3v3_current float,
            eps5v_current float,
            spx_voltage float,
            spx_pos_current float,
            spx_neg_current float,
            spx_pos_temp1 float,
            spy_voltage float,
            spy_pos_current float,
            spy_neg_current float,
            spz_voltage float,
            spz_pos_voltage float,
            spz_pos_temp2 float,
            powermode int)''')

        self.connection.commit()
